import socket
global s
import msvcrt
import time
import os
import sys
from threading import Thread
s = socket.socket()
def inputThread(username):
    while True:
        print(f"\033[{20-1};{0}H")
        msg = input(": ")
        parsedData = "ROOM#MESSAGE#{}#{}".format(username,msg).encode("utf-8")
        s.send(parsedData)
def inRoomPage():
    print("/===== Welcom in the room =====\\")
    buffer = ["" for _ in range(20)]
    out = False
    index = -1
    while True:
        recvData = s.recv(2048).decode("utf-8")
        if len(recvData) > 0:
            print(recvData)
        if out:
            print("Leaving")
def HandleInRoomThreads(username):
    inputT = Thread(target=inputThread,args=[username])
    inputT.start()
    recvT = Thread(target=inRoomPage)
    recvT.start()
    pass
def JoinRoom(username):
    cc()
    print("=====JOIN ROOM=====")
    print("Please enter the room code!")
    code = input("CODE: ")
    print()
    sendData = "ROOM#JOIN#{}#{}".format(code,username).encode("utf-8")
    s.send(sendData)
    reply = s.recv(1024).decode("utf-8")
    h,r = reply.split("#")
    if h == "JOIN":
        if bool(int(r)):
            print("JOINED")
            HandleInRoomThreads(username)
            a = input()
        else:
            print(f"No room has found on code: {code}")
    else:
        pass
def CreateRoom(username):
    pass
def LoggedInOptions(username):
    print("="*10)
    options = ["Join Room","Create Room","Exit"]
    functOptions =[JoinRoom,CreateRoom,ExitPage]
    cc()
    opts = 0
    index = 0
    print("/=====***======\\")
    printOption(options,index)
    while opts != 3:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            cc()
            print("/=====***======\\")
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
    functOptions[abs(opts)%3](username)

def cc():
    os.system("cls")
def LoginPage():
    global s
    cc()
    options = ["Username: ","Password: "]
    print("===== Login Page =====")
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
    print("\n")
    if header == "LOGIN":
        if bool(int(logged)):
            print("[+] Logged Successfuly")
            time.sleep(1)
            LoggedInOptions(usr)
            cc()
        else:
            print("[-] Wrong Username or password!")
            time.sleep(1)
            WelcomePage()
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
    functOptions[abs(opts)%3]()

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