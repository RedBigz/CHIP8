"""
RedBigz's Chip-8 Emulator

| Opcodes
Visit [CHIP-8 Opcode list (Wikipedia)](https://en.wikipedia.org/wiki/CHIP-8\#Opcode_table) for the opcode list.

| Compiling assembly code for the CHIP-8
In CMD, type py assembler.py in.s or python assembler.py in.asm to compile to out.bin.

Syntax
mov VX, val
regdump VX
regload VX

| Compiling machine code for the CHIP-8
You can use a hex editor like HxD to write the opcodes by hand, or modify createcode.py to write the opcodes.

Syntax for createcode.py
b"\xFF\x55" 0xFF55 Opcode (regdump V0-VF)
"""

class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

from threading import Thread as t
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import sys, pygame
import random
from time import sleep
import winsound
import tkinter
import tkinter.filedialog
import ntpath, time
beep = lambda: winsound.Beep(500,166)

if "-d" in sys.argv:
    print(
        colours.HEADER+"\b\b\b\b\bRedBigz's Chip-8 VM Documentation\n"+colours.ENDC+
        "\b\b\b\b"+(""+colours.UNDERLINE+colours.BOLD+colours.OKBLUE+"\b\b\b\b\b\b\b\b\b\b\b\b\b\bhttps://en.wikipedia.org/wiki/CHIP-8\#Opcode_table\n"+colours.ENDC)+"\b\b\b\bUse the createcode.py script to write machine code by hand""\nUse the assembler.py script to compile chip-8 code from assembly language"
        "\n"+colours.WARNING+"\b\b\b\b\b[Note: the assembler is ONLY used to modify memory and (dump/load) to/from memory]"+colours.ENDC
    )
    exit()

root = tkinter.Tk()
root.withdraw()

def loc(lst, k):
    for _, i in enumerate(lst):
        if i == k:
            return _

def getArgVal(switch, default=0):
    if switch in sys.argv:return sys.argv[loc(sys.argv, switch)+1]
    else:return default

verbose = ("-v" in sys.argv) or ("--verbose" in sys.argv)
instpf = getArgVal("-s", 128)

stimer = 0
dtimer = 0
ex=False
mem = [0] * 4096
registers = [0] * 16
PC = 0x200
I = 0
opcode = 0
clock = pygame.time.Clock()
zoom = int(sys.argv[loc(sys.argv, "-z")+1]) if "-z" in sys.argv else 10

def load_rom(path):
    try:
        with open(path, "rb") as file:
            for index, value in enumerate(file.read()):
                mem[0x200 + index] = value
    except IndexError:
        print("File too large! (Over 3.6kB size for program!)")
        exit()

def draw_pixel(x, y):
    #Draws pixel onto screen
    if (x < 64 and y < 32):
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect((x*zoom)+1, (y*zoom)+1, zoom, zoom))
    else:
        pygame.draw.rect(window, (255, 255, 255), pygame.Rect((x-64*zoom)+1, ((y-32)*zoom)+1, zoom, zoom))

def run_rom():
    global stimer
    global dtimer
    global status
    sleep(0.5)
    OldPC = 0
    PC = 0x200
    I = 0
    done = False
    while not done:
        oldtime = time.time()
        opcode = (mem[PC] << 8) | mem[PC+1]
        x = (opcode & 0xf00) >> 8
        y = (opcode & 0xf0) >> 4
        xnnn = (opcode & 0xfff)
        xxnn = (opcode & 0xff)
        xxxn = (opcode & 0xf)
        f = str(hex(opcode))[2]
        PC += 2
        icode = str(hex(opcode))[2:]
        print(hex(PC), icode)
        if icode == "e0":
            window.fill((0,0,0))
        elif icode == "ee":
            PC = OldPC
            if verbose:print("Debug : Returned to main")
        elif f == "1": #Jump to address in memory (1NNN)
            PC = xnnn
            if verbose:print(f"Debug : Jumped to address {hex(xnnn)}")
        elif f == "2":
            OldPC = PC
            PC = xnnn
            if verbose:print(f"Debug : Jumping to subroutine at {hex(xnnn)}")
        elif f == "3": #Vx==xxnn: skip (3XNN)
            if registers[x] == xxnn:
                PC += 2
        elif f == "4": #Vx!=xxnn: skip (4XNN)
            if registers[x] != xxnn:
                PC += 2
        elif f == "5": #Vx==Vy: skip (5XY0)
            if registers[x] == registers[y]:
                PC += 2
        elif f == "6": #MOVL $xxnn, %Vx
            registers[x] = xxnn
            if verbose:print(f"Debug : Register {x} set to {registers[x]}")
        elif f == "7": #ADDL $nn, %Vx
            registers[x]+=xxnn
            if verbose:print(f"Debug : Register {x} set to {registers[x]}")
        elif f == "8": #Math, BitOps etc.
            b = xxxn
            if b == 0: #MOVL %Vy, %Vx
                registers[x] = registers[y]
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 1: #BitOp Or
                registers[x] = registers[x] | registers[y]
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 2: #BitOp And
                registers[x] = registers[x] & registers[y]
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 3: #BitOp xor
                registers[x] = registers[x] ^ registers[y]
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 4: #ADDL %Vy, %Vx
                registers[x]+=registers[y]
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 5:
                registers[x]-=registers[y]
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 6:
                registers[x]>>1
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 7:
                registers[x]=registers[y]-registers[x]
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 0xE:
                registers[x]<<=1
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
        elif f == "9":
            if registers[x] != registers[y]:
                PC+=2
        elif f == "a":
            I = xnnn
        elif f == "b":
            PC = registers[0] + xnnn
        elif f == "c":
            registers[x] = random.randrange(1,256)&xxnn
            if verbose:print(f"Debug : Register {x} set to {registers[x]}")
        elif f == "d":
            height = xxxn
            for i in range(height+1):
                xa=-1
                for bit in ("0"*(8-len(str(bin(mem[I+i]))[2:])))+(str(bin(mem[I+i]))[2:]):
                    xa+=1
                    if bit == "1":
                        draw_pixel(x+xa, y+i)
        elif f == "e":
            if xxnn == 0x9E:
                if pressedlist[registers[x]]:
                    PC += 2
            elif xxnn == 0xA1:
                if not pressedlist[registers[x]]:
                    PC += 2
        elif f == "f":
            b=xxnn
            if b == 7:
                registers[x] = dtimer
            elif b == 0x0A:
                try:
                    keyFound=False
                    key=0
                    while not keyFound:
                        for i in pressedlist:
                            if pressedlist[i]:
                                key = i
                                keyFound = True
                except NameError:
                    sleep(2)
                    keyFound=False
                    key=0
                    while not keyFound:
                        for i in pressedlist:
                            if pressedlist[i]:
                                key = i
                                keyFound = True
                
                registers[x] = key
                if verbose:print(f"Debug : Register {x} set to {registers[x]}")
            elif b == 0x15:
                dtimer = registers[x]
            elif b == 0x18:
                stimer = registers[x]
            elif b == 0x1E:
                I += registers[x]
            elif b == 0x55: #Dump registers to memory
                for i in range(x+1):
                    mem[i+I] = registers[i]
                
                if verbose:print("Debug : Dumped all registers into memory.")    
            
            elif b == 0x65: #Load registers from memory
                for i in range(x+1):
                    registers[i] = mem[i+I]
                
                if verbose:print("Debug : Loaded registers from memory.")

        else:
            if xnnn != 0 and f != "0":
                if verbose:print(f"Error : Opcode ({hex(PC-2)}) Failed to execute.\nOpcode : {icode}")
        
        if PC == 4096:
            done = True
        
        if ex:exit()

    status = "Halted"

def soundtimer():
    global stimer
    while True:
        if stimer > 0:  
            t(target=beep).start()
            stimer -= 1

        sleep(1/60)

        if ex:exit()

def delaytimer():
    global dtimer
    while True:
        if dtimer > 0:
            dtimer -= 1
        
        sleep(1/60)
        if ex:exit()

if __name__ != "__main__":sys.exit()

fname = tkinter.filedialog.askopenfilename(filetypes=[
    ("Chip-8 ROMs","*.ch8;*.bin;*.chip8")
])
root.deiconify()
try:load_rom(fname)
except FileNotFoundError:exit()
root.destroy()
pygame.init()

window = pygame.display.set_mode((64*zoom,32*zoom))
cursor = (
    "..XX    ",
    ". X     ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        ",
    "        "
    )
cursor = pygame.cursors.compile(cursor)
pygame.mouse.set_cursor((8, 8), (0, 0), *cursor)
pygame.display.set_icon(pygame.image.load("Icon.png"))
status = "Running"
pygame.display.set_caption(f"CVM 1.0: {ntpath.basename(fname)} ({status})")
t(target=run_rom).start()
t(target=soundtimer).start()
t(target=delaytimer).start()

pressed = pygame.key.get_pressed()
pressedlist = {
        0: pressed[pygame.K_0],
        1: pressed[pygame.K_1],
        2: pressed[pygame.K_2],
        3: pressed[pygame.K_3],
        4: pressed[pygame.K_4],
        5: pressed[pygame.K_5],
        6: pressed[pygame.K_6],
        7: pressed[pygame.K_7],
        8: pressed[pygame.K_8],
        9: pressed[pygame.K_9],
        0xa: pressed[pygame.K_a],
        0xb: pressed[pygame.K_b],
        0xc: pressed[pygame.K_c],
        0xd: pressed[pygame.K_d],
        0xe: pressed[pygame.K_e],
        0xf: pressed[pygame.K_f]
    }


a=True
cycles = 60 # 60Hz

while a:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            a=False

    pressed = pygame.key.get_pressed()
    pressedlist = {
        0: pressed[pygame.K_0],
        1: pressed[pygame.K_1],
        2: pressed[pygame.K_2],
        3: pressed[pygame.K_3],
        4: pressed[pygame.K_4],
        5: pressed[pygame.K_5],
        6: pressed[pygame.K_6],
        7: pressed[pygame.K_7],
        8: pressed[pygame.K_8],
        9: pressed[pygame.K_9],
        0xa: pressed[pygame.K_a],
        0xb: pressed[pygame.K_b],
        0xc: pressed[pygame.K_c],
        0xd: pressed[pygame.K_d],
        0xe: pressed[pygame.K_e],
        0xf: pressed[pygame.K_f],
        "cycle_speed": pressed[pygame.K_x],
        "cycle_slow": pressed[pygame.K_z]
    }

    if pressedlist["cycle_speed"]:
        cycles += 1
    elif pressedlist["cycle_slow"]:
        cycles -= 1

    pygame.display.flip()
    clock.tick(cycles)

    pygame.display.set_caption(f"CVM 1.0: {ntpath.basename(fname)} ({status}) [{cycles} Hz]")

pygame.quit()
ex=True
sys.exit()
