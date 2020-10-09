# CHIP8
A CHIP-8 Emulator made in Python and PyGame.
### Opcodes
Click [Here](https://en.wikipedia.org/wiki/CHIP-8) to look at the CHIP-8 architecture and an opcode table for the CHIP-8 VM.
### Before you run the program for the first time
Before you run the program for the first time, type ```pip install pygame``` into the command prompt.
On linux, type ```pip3 install pygame``` into the terminal emulator.
### CHIP-8 tools
+ ```Emulator.pyw``` : the emulator.
+ ```compile.py``` : the compiler, syntax below.
+ ```decompile.py``` : the decompiler (decompiles into hex data).

### Compiler Syntax
When you read the compile.py file, you should see this:
```
with open("out.bin","wb") as file:
  file.write(
    #Stuff here
  )
```
Inside ```file.write``` put your opcodes like this:
```b"\x12\x34"```
