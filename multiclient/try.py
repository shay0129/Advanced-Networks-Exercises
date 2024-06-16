import msvcrt

END_MSG = '\r'
msg = ""
x = True
while x:
    if msvcrt.kbhit():
        ch = msvcrt.getch().decode()
        if ch == END_MSG:
            x = False
        else:
            print(ch, end = "", flush=True)
            msg += ch

print(msg)