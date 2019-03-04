#! /usr/bin/env python3
# A simple program implementing a server for a basic file transfer.

import sys
from socket import *
from select import select
import sys, os, re, time

global cAddr
global reqFile
global seqNumber
global line

# The address and port of the server - socket, too
sAddr = ("",50000)
sSocket = socket(AF_INET, SOCK_DGRAM)

# Doesn't know the name of the file yet!
reqFilename = ""

def getting(sSocket):
    ackn,cAddr = sSocket.recvfrom(100)
    print("%s recieved." % ackn)

print("Binding...")
sSocket.bind(sAddr)
print("Ready for request.")

#Wait for client to request file.
request, cAddr = sSocket.recvfrom(100)
print("from %s: rec'd <%s>" % (repr(cAddr), repr(request)))

seqNumber, msgLen, reqFilename = request.decode().split(':')

# Open the file and send it to client line by line.
reqFile = open(reqFilename, "r")

readSelect = {}
sendSelect = {} # NOT USED.
errSelect = {}
timeout = 5
tries = 0 #if tries == 3, exit program

readSelect[sSocket] = getting

line = reqFile.readline()
line = str(seqNumber) + ":5:" + line
seqNumber = int(seqNumber)
sSocket.sendto(line.encode(), cAddr)
print("sent %s" % line)
status = "sentMsg" #possible states: sending, sentMsg

while 1:
    rReady, sReady, error = select( list(readSelect.keys()),
                                    list(sendSelect.keys()),
                                    list(errSelect.keys()),
                                    timeout)
    if not rReady and not sReady and not error:

        if tries != 3 and status == "sentMsg":
            print("timeout. Retransmitting.")
            seqNumber = int(seqNumber)
            sSocket.sendto(line.encode(), cAddr)
            tries += 1
            
        if tries == 3:
            print("No response. Exiting...")
            exit()
    
            
    for sock in rReady:
        tries = 0
        seqNumber += 1
        readSelect[sSocket](sock)
        line = reqFile.readline()
            
        if line.strip() == "":
            print("File sent. Sending end symbol...")
            sSocket.sendto("#".encode(),cAddr)
            exit()

        
        line = str(seqNumber) +":5:"+line
        sSocket.sendto(line.encode(), cAddr)
            
    

        

    
