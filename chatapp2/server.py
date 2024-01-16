from threading import Thread
import socket
ip = "127.0.0.1"
port = 5500
server = None
clients = {}
buffersize = 4096

def setup():
    global server
    global ip
    global port
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(10)
    print("server started")
    acceptClient()

def acceptClient():
    global server
    global clients
    while True:
        client,address = server.accept()
        print(client, address)
        clientName = client.recv(4096).decode()
        clients[clientName] = {
            "client": client,
            "address": address,
            "connectedwith": "",
            "filename":"" ,
            "filesize":4096
        }
        print(clientName)
        thread2 = Thread(target=handleClients, args=(client, clientName))
        thread2.start()

def handleClients(client, clientname):
    global clients
    global server
    global buffersize
    client.send("welcome to the chat".encode("utf-8"))
    while True:
        try:
            buffersize = clients[clientname]["filesize"]
            details = client.recv(buffersize).decode()
            print(details, "3")
            if(details):
                print(details, "2")
                handlemsg(client, details, clientname)
        except:
            pass

def handlemsg(client, details, clientname):
    print(details, "1")
    if(details == "showlist"):
        handlelist(client)
    if(details[:7] == "connect"):
        connectUser(details, client, clientname)
    if(details[:10] == "disconnect"):
        disconnectuser(details, client, clientname)

def handlelist(client):
    print(client)
    global clients
    clientcount=0
    for i in clients:
        clientcount+=1
        clientaddress = clients[i]["address"][0]
        connectedwith = clients[i]["connectedwith"]
        print(connectedwith, "connected with")
        message = ""
        if(connectedwith):
            message = f"{clientcount}, {i}, {clientaddress}, connected with, {connectedwith}, tiul, \n"
        else:
            message = f"{clientcount}, {i}, {clientaddress}, available, now, tiul, \n"
        client.send(message.encode())
        print(message)

def connectUser(details, client, clientname):
    global clients
    selectedClient = details[8:].strip()
    print(selectedClient)
    if(selectedClient in clients):
        if(not clients[clientname]["connectedwith"]):
            clients[selectedClient]["connectedwith"] = clientname
            clients[clientname]["connectedwith"] = selectedClient
            otherclientssocket = clients[selectedClient][client]
            print(otherclientssocket)
            # message = f"hi {selectedClient}, {clientname} is connected with you"
            otherclientssocket.send("working".encode())
            # msg = f"you have succefully connected with {selectedClient}"
            client.send("working".encode())
        else:
            otherclientsname = clients[clientname]["connectedwith"]
            message2 = f"you have already connected to {otherclientsname}"
            client.send(message2.encode())

def disconnectuser(details, client, clientname):
    global clients
    selectedClient = details[11:]
    print(selectedClient)
    if(selectedClient in clients):
        
        clients[selectedClient]["connectedwith"] = ""
        clients[clientname]["connectedwith"] = ""
        otherclientssocket = clients[selectedClient][client]
        message = f"hi {selectedClient}, {clientname} has disconnected with you"
        otherclientssocket.send(message.encode())
        msg = f"you have succefully disconnected with {selectedClient}"
        client.send(msg.encode())

    
thread1 = Thread(target=setup)
thread1.start()


