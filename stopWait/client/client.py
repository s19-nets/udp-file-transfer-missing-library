#! /usr/bin/env python3
# Simple client program for getting a file from a server.

from socket import *
import sys, re, os, time
from select import select

global status
global ack
global ackCounter
global reqFilename

# Default server address
sAddr = ('localhost',50000)

# Client socket
cSocket = socket(AF_INET, SOCK_DGRAM)
request = "none"
cSocket.setblocking(False)

def getting(cSocket, reqFile):
    ack = str(ackCounter)+":100:"+ "ACKN"
    response, addr = cSocket.recvfrom(100)
    print("Recieved " + str(response))
    
    if response.decode() == "#":
        print("File complete! Exiting...")
        exit()
        
    reqFile.write(response.decode())
    print("Sending " + ack)
    cSocket.sendto(ack.encode(), sAddr)
    status = "downloading"

ackCounter = 0
request = input("Request a file from the server: ") 
print("Requesting file: ",request)
reqFilename = str(ackCounter) + ":100:" + request
print("sending " + reqFilename)

# Create a copy of the file.
reqFile = open(request, "w")
print("Downloading file...")
status = "idle"

readSelect = {}
sendSelect = {} # NOT USED.
errSelect = {}
timeout = 5
tryCounter = 0

readSelect[cSocket] = getting
status = 'firstMsg'

while 1:
    rReady, sReady, error = select(list(readSelect.keys()),
                          list(sendSelect.keys()),
                          list(errSelect.keys()),
                          timeout)
    
    if not rReady and not sReady and not error:
        
        if tryCounter != 3 and status == "firstMsg":
            print("timeout. Retransmitting File Name.")
            cSocket.sendto(reqFilename.encode(), sAddr)
            tryCounter += 1
            
        if tryCounter != 3 and status == "downloading":
            print("timeout. Retransmitting.")
            tryCounter+=1
            cSocket.sendto(ack.encode(), sAddr)
            
        if tryCounter == 3:
            print("No response. Exiting...")
            exit()
            
    for sock in rReady:
        tryCounter = 0
        ackCounter += 1
        status = "downloading"
        readSelect[cSocket](sock,reqFile)
