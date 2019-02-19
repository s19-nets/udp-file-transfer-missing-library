#! /usr/bin/env python3
# Simple client program for getting a file from a server.

from socket import *
import sys, re, os

# Default server address
sAddr = ('localhost',50000)

# Client socket
cSocket = socket(AF_INET, SOCK_DGRAM)
request = "none"


while (request is not "exit"):

    request = input("Request a file from the server: ") 

    print("Requesting file: ",request)
    reqFilename = request

    # Send the name of the file to the server.
    cSocket.sendto(reqFilename.encode(),sAddr)

    # Recieve the first line of the file!
    response, addr = cSocket.recvfrom(100)

    # Create a copy of the file.
    reqFile = open(reqFilename, "w")
    print("Downloading file...")

    # Recieve file line by line 'till server says it's done.
    while response.decode() != "good":
        reqFile.write(response.decode())
        response, addr = cSocket.recvfrom(100)
        cSocket.sendto("Woo!".encode(),sAddr)

    print("File recieved!")
