import socket
import threading

nick = input("Choose a Nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost",56565))

def recieve():
    while True:
        try:
            m = client.recv(1024).decode('ascii')
            if m == "NICK":
                client.send(nick.encode("ascii"))
            elif m == "DISC":
                print("Disconnected!")
                client.close()
                break
            else:
                print(m)
        except:
            print("Disconnected, Error occured")
            client.close()
            break

def write():
    while True:
        m = f'{nick}: {input("")}'
        client.send(m.encode("ascii"))
        if(m == f"{nick}: disc()"):
            break

t1 = threading.Thread(target=recieve)
t2 = threading.Thread(target=write)
t1.start()
t2.start()

