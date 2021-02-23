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
def recieveData():
    print("Yes")
    while True:
        for conn in connections:
            if conn.isconnected:
                data = conn.socket.recv(1024)
                print(data)
                if data:
                    print(data)
    pass
def handleThreads():
    handleConnections = Thread(target=waitingClientConnection)
    handleConnections.start()
    handleDatarecv = Thread(target=recieveData)
    handleDatarecv.start()
def main():
    createServer()
    handleThreads()
    pass
main()