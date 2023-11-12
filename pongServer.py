# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import random

currentConnections=[]

def handle_client(clientSocket:socket, clientAddress:str):
    try:
        message = clientSocket.recv(1024).decode()
        print(f"Client {clientAddress} sent: {message}")

        threading.wait()
        clientSocket.send("GS".encode())

        clientSocket.send("640".encode())
        clientSocket.send("480".encode())
        clientSocket.send("left".encode())

        msg = ""
        while msg != "quit": 
            msg = clientSocket.recv(1024).decode() #Paddle pos receive
            print(f"Client {clientAddress} sent: {msg}")
            clientSocket.send(msg.encode())

    except Exception as e:
        print(f"Error with client {clientAddress}: {str(e)}")

    finally:
        clientSocket.close()
        print(f"Connection with client {clientAddress} closed.")

def chooseplayers(total:int):
  p=random.sample(range(0,total),2)
  return(p)

def choosesides():
  return(random.sample(["left","right"],2))

def createThread(clientSocket:socket,clientAddress:str):
    client_thread = threading.Thread(target=handle_client, args=(clientSocket, clientAddress))
    client_thread.start()
    return(client_thread)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("10.47.189.133", 12321)) #MY IP
server.listen(5)

try:
    while True:
        clientSocket, clientAddress = server.accept()

        t=createThread(clientSocket,clientAddress)
        currentConnections.append(t)
        print(f"Thread {len(currentConnections)} started with {clientAddress}")

        if(threading.active_count()>=2):
            notify_all()

finally:
    server.close()

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games