#! /usr/bin/env python3
# Simple client program for getting a file from a server.

from socket import *
import sys, re, os, time
from select import select

global status

# Default server address
sAddr = ('localhost',50000)

# Client socket
cSocket = socket(AF_INET, SOCK_DGRAM)
cSocket.setblocking(False)
request = "none"
ack = "ACKN"


def getting(cSocket, reqFile):
    ack = "ACKN"
    response, addr = cSocket.recvfrom(100)
    if response.decode() == "#":
        print("File complete! Exiting...")
        exit()
        
    reqFile.write(response.decode())
    sending(ack.encode(), addr)
    
def sending(sock,reqFile):
    ack = "ACKN"
    print("Sending ACK")
    cSocket.sendto(ack.encode(), sAddr)
    status = 'sentMsg'


request = input("Request a file from the server: ") 
print("Requesting file: ",request)
reqFilename = request


# Create a copy of the file.
reqFile = open(reqFilename, "w")
print("Downloading file...")
status = "idle"

readSelect = {}
sendSelect = {}
errSelect = {}
timeout = 5
tryCounter = 0

readSelect[cSocket] = getting
#sendSelect[cSocket] = sending //non-operational

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
        print("Message recieved.")
        tryCounter = 0
        status = "downloading"
        readSelect[cSocket](sock,reqFile)
        
