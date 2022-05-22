import socket
import threading

host = "localhost"
port = 56565

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
nicks = []

def disconnecthandler(client):
    i = clients.index(client)
    client.send("DISC".encode('ascii'))
    clients.remove(client)
    client.close()
    nickname = nicks[i]
    sendmsg(f"{nickname} left the chat.".encode('ascii'))
    print(f"{nickname} disconnected!")
    nicks.remove(nickname)

def sendmsg(m):
    for client in clients:
        client.send(m)

def conhandler(client):
    while True:
        try:
            m = client.recv(1024)
            if(m.decode('ascii') == f"{nicks[clients.index(client)]}: disc()"):
                disconnecthandler(client)
                break
            else:
                sendmsg(m)
        except:
            disconnecthandler(client)
            break

def recieve():
    while True:
        client, adr = server.accept()
        print(f"{str(adr)} Connected")
        client.send('NICK'.encode('ascii'))
        nick = client.recv(1024).decode('ascii')
        nicks.append(nick)
        clients.append(client)

        print(f"New User: {nick}")
        sendmsg(f"{nick} joined the chat".encode('ascii'))
        client.send(f"Welcome to the chat {nick}".encode('ascii'))

        thread = threading.Thread(target=conhandler,args=(client,))
        thread.start()

print("Chat started")
recieve()