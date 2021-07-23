import socket
import threading

PORT = 50020
HOST=socket.gethostbyname(socket.gethostname())

ADDRESS=(HOST,PORT)

FORMAT="utf-8"

clients=[]
names=[]

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(ADDRESS)

def startchat():
    print("Server is working on "+ HOST)
    server.listen()
    while True:
        connection,addr=server.accept()
        connection.send("NAME".encode(FORMAT))

        name = connection.recv(1025).decode(FORMAT)
        names.append(name)

        clients.append(connection)

        print(f"Name is: {name}")
        #print(f"Client is : {connection}")
        broadcastMessage(f"{name} has joined the group ".encode(FORMAT))

        connection.send("Connection successfull".encode(FORMAT))

        thread = threading.Thread(target=recieve,args=(connection,addr))

        thread.start()
        print(f"active connection {threading.activeCount()-1}")


def recieve(connection,addr):
    print(f"New Connection {addr}")

    connected=True

    while connected:
        message=connection.recv(1025)
        broadcastMessage(message)

    connection.close()

def broadcastMessage(message):
    for client in clients:
        client.send(message)

startchat()