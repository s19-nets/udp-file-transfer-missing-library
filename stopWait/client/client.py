#! /usr/bin/env python3
# Simple client program for getting a file from a server.

from socket import *
import sys, re, os, time
from select import select

global status
global ack
global ackCounter

# Default server address
sAddr = ('localhost',50000)

# Client socket
cSocket = socket(AF_INET, SOCK_DGRAM)
request = "none"
cSocket.setblocking(False)

def getting(cSocket, reqFile):
    ack = str(ackCounter)+":"+ str(len("ACKN")) + ":ACKN"
    msg, addr = cSocket.recvfrom(100)
    print("Recieved " + str(msg))
    
    if msg.decode() == "#":
        print("File complete! Exiting...")
        exit()
    msg = msg.decode()
    seqNum, msgLen, msg = msg.split(':')
    reqFile.write(msg)
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
tryCounter = 0 # if tries == 3, give up

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
            ack = str(ackCounter)+":100:"+ "ACKN"
            cSocket.sendto(ack.encode(), sAddr)
            
        if tryCounter == 3:
            print("No response. Exiting...")
            exit()
            
    for sock in rReady:
        tryCounter = 0
        ackCounter += 1
        status = "downloading"
        readSelect[cSocket](sock,reqFile)
