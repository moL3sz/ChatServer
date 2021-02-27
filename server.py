import socket 
from threading import Thread
import time
global s
class Connection:
    def __init__(self,sock,addr,isconnected):
        self.socket = sock
        self.addr = addr
        self.isconnected = isconnected
connections = []
rooms = {"123":[]}
def checkLogin(user,passw):
    data = [sor.strip().split("#") for sor in open("database.dat").readlines()]
    for u,p in data:
        if u == user and passw == p:
            return True
    return False
def createServer():
    global s
    try:
        s = socket.socket()
        s.bind(("localhost",4444))
        s.listen(0)
        print("[+] A server has created successfully!")
        pass
    except Exception as msg:
        print("[-] An error has occured during a server creation")
        print("[*] Retring in 5 seconds!")
        print(msg)
        time.sleep(5)
        createServer()
def waitingClientConnection():
    global s
    while True:
        con,addr = s.accept()
        connection = Connection(con,addr,True)
        print(f"[*] Connection from: {addr[0]}:{addr[1]}")
        connections.append(connection)
def inRoomHandle():
    while True:
        for k,m in zip(rooms.keys(),rooms.values()):
            for conn,username in m:
                data = conn.socket.recv(2048).decode("utf-8")
                if len(data) > 0:
                    print(data)
def recieveData():
    print("Yes")
    while True:
        for conn in connections:
            if conn.isconnected:
                data = conn.socket.recv(1024)
                dData = data.decode("utf-8")
                fData =dData.split("#")
                if fData[0] == "LOGIN":
                    if checkLogin(fData[1],fData[2]):
                        conn.socket.send(b"LOGIN#1")
                    else:
                        conn.socket.send(b"LOGIN#0")
                if fData[0] == "ROOM":
                    if fData[1] == "JOIN":
                        code = fData[2]
                        if code in rooms.keys():
                            rooms[fData[2]].append((conn,fData[3]))
                            conn.socket.send(b"JOIN#1")
                        else:
                            conn.socket.send(b"JOIN#2")
    pass
def handleThreads():
    handleConnections = Thread(target=waitingClientConnection)
    handleConnections.start()
    handleDatarecv = Thread(target=recieveData)
    handleDatarecv.start()
    handleRoomMessages = Thread(target=inRoomHandle)
    handleRoomMessages.start()
def main():
    createServer()
    handleThreads()
    pass
main()