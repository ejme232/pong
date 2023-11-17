# =================================================================================================
# Contributing Authors:	    Evan Meyers, Connor Day
# Email Addresses:          evan.meyers@uky.edu, connor.day@uky.edu
# Date:                     11/17/2023
# Purpose:                  Contains code for running server-side operations.
# =================================================================================================

import socket
import threading
import random

# Define the game information
screen_width = 640  # Set the desired width
screen_height = 480  # Set the desired height

# Store client sockets
client_sockets = []

# Maintain a counter for assigning sides to clients
side_counter = 0

# Default gamestate values. Should get updated as soon as the game starts
gamedict={"Lpos":'1',
          "Rpos":'1',
          "Ballx":'0',
          "Bally":'0',
          "Ballxvel":'0',
          "Ballyvel":'0',
          "Lscore":'0',
          "Rscore":'0',
          "Sync":'-1'}

# Authors:       Connor Day, Evan Meyers
# Purpose:       Update the game state dictionary based on the received message
# Pre:           The message is formatted correctly and contains game state information
# Post:          The game state dictionary is updated with the new information
def update_gamedict(msg: str) -> None:
    #Parses msg into a list of strs
    recSide, recPos, recBallx, recBally, recBallxv, recBallyv, recLscore, recRscore, recSync=msg.split(",")
    if(int(recSync)>=int(gamedict["Sync"])): #If this passes, the info is new! UPDATE
        if(recSide=='left'):
            gamedict['Lpos']=recPos
        if(recSide=='right'):
            gamedict['Rpos']=recPos
        gamedict['Ballx']=recBallx
        gamedict['Bally']=recBally
        gamedict['Ballxvel']=recBallxv
        gamedict['Ballyvel']=recBallyv
        gamedict['Lscore']=recLscore
        gamedict['Rscore']=recRscore
        gamedict['Sync']=recSync

# Authors:       Connor Day, Evan Meyers
# Purpose:       Handle a client connection for a simple game server
# Pre:           The server is running and listening for client connections
# Post:          The client is connected, and the game state is communicated between clients
def handle_client(clientSocket: socket.socket, clientAddress: str) -> None:
    # This method is fired when the join button is clicked
    global client_sockets, side_counter

    # Determine the side for the current client
    if side_counter == 0:
        side="left"
    else: 
        side="right"
    side_counter = (side_counter + 1) % 2  # Toggle between 0 and 1

    # Add the client socket to the list
    client_sockets.append(clientSocket)
    #print(f"added {clientSocket}") #Prints connected client (for debugging)
    
    try:
        clientSocket.send(f"You're connected.".encode()) #Tell client they're connected

        while len(client_sockets) < 2:  # Wait until there are 2 client sockets
            continue
        msg=""

        if len(client_sockets) == 2:  # There are 2 now! Start the game
            clientSocket.send("Ready".encode()) #Tell client the game is ready to start
            while(msg!="Starting"): #When the client responds, send data
                msg=clientSocket.recv(1024).decode()
            # Send game info to all clients
            game_info = f"{screen_width},{screen_height},{side}"
            clientSocket.send(game_info.encode())
            while msg != "quit": #THE GAME IS BEING PLAYED!!!
                msg = clientSocket.recv(1024).decode() #Paddle pos receive
                update_gamedict(msg) #Update game state information stored on server

                # Send updated game state to all clients
                game_state = f"{gamedict['Lpos']},{gamedict['Rpos']},{gamedict['Ballx']},{gamedict['Bally']},{gamedict['Ballxvel']},{gamedict['Ballyvel']},{gamedict['Lscore']},{gamedict['Rscore']},{gamedict['Sync']}"
                with lock: #Ensure that clients only edit gamedict one at a time to avoid interleaving
                    clientSocket.send(game_state.encode())
                
                #print(f"Sent game_state: {game_state}") #Print sent game state (for debugging)

    except Exception as e:
        #If error, print why!
        print(f"Error with client {clientAddress}: {str(e)}")

    finally:
        # Remove the client socket from the list
        client_sockets.remove(clientSocket)
        clientSocket.close()
        print(f"Connection with client {clientAddress} closed.")

# Authors:       Connor Day, Evan Meyers
# Purpose:       Create a thread for the given socket and address to handle a client connection
# Pre:           The client socket and address are provided
# Post:          A new thread is created to handle the client connection
def createThread(clientSocket: socket.socket, clientAddress: str) -> None:
    #   Purpose:        Creates thread for the given socket and address
    #   clientSocket: Contains socket information for this client
    #   clientAddress:Contains address for this client as a str object
    client_thread = threading.Thread(target=handle_client, args=(clientSocket, clientAddress))
    client_thread.start()

#Server set-up
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
myip=socket.gethostbyname(socket.gethostname()) # Stores user's ip
print(myip) #So we can find the IP easier
server.bind((myip, 12321))
server.listen(5)
lock=threading.Lock()

try:
    while True: #Server constantly accepts new connections
        clientSocket, clientAddress = server.accept()
        createThread(clientSocket,clientAddress) #When client connects, assign to a thread
        print(f"Thread {threading.active_count()} started with {clientAddress}")

finally:
    server.close()

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games