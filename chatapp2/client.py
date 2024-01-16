from tkinter import *
from tkinter import ttk
from threading import Thread
import socket

ip = "127.0.0.1"
port = 5500
server = None

name = None
listbox = None
textarea = None
labelChat = None
msg = None
bufferSize = 4096

def setup():
    global server
    global ip
    global port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((ip,port))
    thread = Thread(target=receivemsg)
    thread.start()
    chatWindow()

def chatWindow():
    global name
    global textarea
    global listbox
    window = Tk()
    window.title("Chat App")
    window.geometry("500x500")
    username = Label(window, text="Enter Name", font=("Arial", 10))
    username.place(x=20, y=10)
    name = Entry(window, width=20, font=("Arial", 15), borderwidth=2)
    name.place(x=100, y=10)
    connectButton = Button(window, text="connect to server", font=("Arial", 12), command=connectServer)
    connectButton.place(x=350, y = 10)
    separtator = ttk.Separator(window, orient="horizontal")
    separtator.place(x=5, y=50, relwidth=1, height=0.2)
    userDetails = Label(window, text="Active users", font=("Arial", 18))
    userDetails.place(x=50, y=60)
    listbox = Listbox(window, height=5, width=50, font=("Arial", 12))
    listbox.place(x=20, y=100)
    scrollbar = Scrollbar(listbox)
    scrollbar.place(relx=1, rely=0, relheight=1)
    scrollbar.config(command=listbox.yview)
    connect = Button(window, text="Connect", font=("Arial", 13), command=connectuser)
    disconnect = Button(window, text="Disconnect", font=("Arial", 13), command=disconnectuser)
    refresh = Button(window, text="Refresh", font=("Arial", 13), command=refreshconnections)
    connect.place(x=350, y=190)
    disconnect.place(x=250, y=190)
    refresh.place(x=180, y=190)
    chatLabel = Label(window, text="Chat window", font=("Arial", 15))
    chatLabel.place(x=20, y=210)
    textarea = Text(window, font=("Arial", 13), width=50, height=5)
    textarea.place(x=20, y=240) 
    scrollbar2 = Scrollbar(textarea)
    scrollbar2.place(relx=1, rely=0, relheight=1)   
    scrollbar2.config(command=textarea.yview)
    attach = Button(window, text="Attach", font=("Arial", 13))
    attach.place(x=20, y=350)
    textmsg = Entry(window, font=("Arial", 13), width=30)
    textmsg.pack()
    textmsg.place(x=90, y=350)
    send = Button(window, text="send", font=("Arial", 13))
    send.place(x=370, y=350)

    window.mainloop()

def connectServer():
    global server
    global name
    username = name.get()
    print(username)
    server.send(username.encode("ascii"))

def receivemsg():
    global server
    global bufferSize
    global textarea
    while True:
        try:
            details = server.recv(bufferSize)
            print(details)
            if("tiul" in details.decode() and "1.0" not in details.decode()):
                namelist = details.decode().split(",")
                print(namelist)
                print(details)
                listbox.insert(namelist[0],namelist[0] + ":" + namelist[1] + ":" + namelist[3] + " " + namelist[4])
                print(namelist[0],namelist[0] + ":" + namelist[1] + ":" + namelist[3] + " " + namelist[4])
            else:
                textarea.insert(END, "\n"+details.decode("ascii"))
                textarea.see("end")
                print(details.decode("ascii"))
        except:
            pass

def refreshconnections():
    global listbox
    global server
    global name
    listbox.delete(0,"end")
    server.send("showlist".encode("ascii"))
    print("showlist")



def connectuser():
    global server
    global listbox
    text = listbox.get(ANCHOR)
    splitText = text.split(":")
    print(splitText)
    message = "connect" + splitText[1] 
    print(message)
    server.send(message.encode())

def disconnectuser():
    global server
    global listbox
    text = listbox.get(ANCHOR)
    splitText = text.split(":")
    print(splitText)
    message = "disconnect" + splitText[1] 
    print(message)
    server.send(message.encode())

setup()



