import socket
global s
import msvcrt
import time
import os
import sys
s = socket.socket()
def cc():
    os.system("cls")
def LoginPage():
    global s
    cc()
    options = ["Username: ","Password: "]
    print("===== Login Page =====")
    i = 0
    usr = input(options[0])
    pwd = ""
    print(options[1],end="",flush=True)
    while True:
        key = msvcrt.getch()
        char = str(key)[2:-1]
        if key == b'\r' or key == b"\xb1":
            break
        else:
            pwd+=char
            print("*",end="",flush=True)
    dataToSend = "LOGIN#{}#{}".format(usr,pwd).encode("utf-8")
    s.send(dataToSend)
    reply = s.recv(1024).decode("utf-8")
    header,logged = reply.split("#")
    if bool(logged):
        print("[+] Logged Successfuly")
    pass
def RegistrationPage():
    pass
def ExitPage():
    cc()
    print("By have a good time!")
    exit(0)
    pass
def printOption(op,x):
    for i,o in enumerate(op):
        if i == x%3:
            print(f"{o} <-")
        else:
            print(o)
def WelcomePage():
    cc()
    options = ["Login","Registrate","Exit"]
    functOptions =[LoginPage,RegistrationPage,ExitPage]
    opts = 0
    index = 0
    print("Welcome on The Chat Server")
    printOption(options,index)
    while opts != 3:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            cc()
            print("Welcome on The Chat Server")
            if key == b'H':
               index -= 1
            if key == b'P':
                index +=1
            if key == b"\r":
                opts = index
                break
            if key == b"\x1b":
                functOptions[-1]()
            printOption(options,index)
    functOptions[opts]()

def connect():
    global s
    addr = "localhost"
    port = 4444
    try:
        s.connect((addr,port))
        return True
    except Exception as msg:
        print(f"[-] Unable to connect to the server! ({addr}:{port})")
        print("[*] Retring in 5 seconds!")
        print(msg)
        time.sleep(5)
        connect()
    return False
def main():
    if connect():
        WelcomePage()


main()