with open(input("File : "), "rb") as file:
    for char in file.read():
        print("b'\\x"+str(hex((char)))[2:]+"'" if len(str(hex((char)))[2:]) == 2 else "b'\\x0"+str(hex((char)))[2:]+"'")