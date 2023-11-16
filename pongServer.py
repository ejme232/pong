# =================================================================================================
# Contributing Authors:	    Evan Meyers, Connor Day
# Email Addresses:          evan.meyers@uky.edu, connor.day@uky.edu
# Date:                     11/17/2023
# Purpose:                  Contains code for running server-side operations.
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import random

# Define the game information
screen_width = 640  # Set the desired width
screen_height = 480  # Set the desired height
side = "left"  # Replace with the actual side information

# Store client sockets
client_sockets = []

gamedict={"Lpos":'',
          "Rpos":'',
          "Ballx":'',
          "Bally":'',
          "Lscore":'',
          "Rscore":'',
          "Sync":''}

def update_gamedict(msg):
    recSide, recPos, recBallx, recBally, recLscore, recRscore, recSync=msg.split(",")
    if(int(recSync)>=int(gamedict["Sync"])): #New info! UPDATE
        if(recSide=='left'):
            gamedict['Lpos']=recPos
        if(recSide=='right'):
            gamedict['Rpos']=recPos
        gamedict['Ballx']=recBallx
        gamedict['Bally']=recBally
        gamedict['Lscore']=recLscore
        gamedict['Rscore']=recRscore
        gamedict['Sync']=recSync


def handle_client(clientSocket:socket, clientAddress:str):
    # Purpose:      This method is fired when the join button is clicked
    # Arguments:
    # clientSocket: Contains socket information for this client
    # clientAddress:Contains address for this client as a str object
    global client_sockets
    # Add the client socket to the list
    client_sockets.append(clientSocket)
    
    try:
        clientSocket.send("You're connected.".encode())
        msg=""

        while(threading.active_count()<3):
            continue

        if(threading.active_count()>=3):
            clientSocket.send("Ready".encode())
            while(msg!="Starting"):
                msg=clientSocket.recv(1024).decode()
            game_info = f"{screen_width},{screen_height},{side}"
            clientSocket.send(game_info.encode())
            msg = ""
            while msg != "quit": #THE GAME IS BEING PLAYED!!!
                msg = clientSocket.recv(1024).decode() #Paddle pos receive
                update_gamedict(msg)

                # Send updated game state to all clients
                game_state = f"{gamedict['Lpos']},{gamedict['Rpos']},{gamedict['Ballx']},{gamedict['Bally']},{gamedict['Lscore']},{gamedict['Rscore']}"
                for socket in client_sockets:
                    socket.send(game_state.encode())

    except Exception as e:
        print(f"Error with client {clientAddress}: {str(e)}")

    finally:
        # Remove the client socket from the list
        client_sockets.remove(clientSocket)
        clientSocket.close()
        print(f"Connection with client {clientAddress} closed.")

def chooseplayers(total:int):
  p=random.sample(range(0,total),2)
  return(p)

def choosesides():
  # Purpose:        Chooses side for each connection randomly
  return(random.sample(["left","right"],2))

def createThread(clientSocket:socket,clientAddress:str):
    #   Purpose:        Creates thread for the given socket and address
    #   clientSocket: Contains socket information for this client
    #   clientAddress:Contains address for this client as a str object
    client_thread = threading.Thread(target=handle_client, args=(clientSocket, clientAddress))
    client_thread.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
myip=socket.gethostbyname(socket.gethostname()) # Stores user's ip (TEST THIS!!)
server.bind((myip, 12321))
server.listen(5)
lock=threading.Lock()

try:
    while True:
        clientSocket, clientAddress = server.accept()
        createThread(clientSocket,clientAddress)
        print(f"Thread {threading.active_count()} started with {clientAddress}")

        if(threading.active_count()>=2):
            threading.Event()

finally:
    server.close()

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games