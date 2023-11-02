# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    # Working on localhost need this

server.bind(("10.47.223.49", 12321))
server.listen(5)


clientSocket, clientAddress = server.accept()




message = clientSocket.recv(1024)               # Expect "Hello Server"

print(f"Client sent: {message.decode()}")

clientSocket.send("200".encode())
clientSocket.send("left".encode())

msg = ""
while msg != "quit":
    msg = clientSocket.recv(1024).decode()          # Received message from client
    print(f"Client sent: {msg}")
    clientSocket.send(msg.encode())



clientSocket.close()
server.close()

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games