with open("out.bin", "wb") as file:
    file.write(
        b'\x60'
        b'\x90'
        b'\x61'
        b'\x90'
        b'\x62'
        b'\xf0'
        b'\x63'
        b'\x90'
        b'\x64'
        b'\x90'
        b'\xf4'
        b'\x55'
        b"\xD0\x04" #Draw
        b'\x60'
        b'\x80'
        b'\x61'
        b'\x00'
        b'\x62'
        b'\x80'
        b'\x63'
        b'\x80'
        b'\x64'
        b'\x80'
        b'\xf4'
        b'\x55'
        b"\xD5\x04"
        )