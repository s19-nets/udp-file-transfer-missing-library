#! /usr/bin/env python3
# A simple program implementing a server for a basic file transfer.

import sys
from socket import *
import sys, os, re, time

global seqNumber

# The address and port of the server - socket, too
sAddr = ("",50000)
srSocket = ("",500001)
sSocket = socket(AF_INET, SOCK_DGRAM) 
srSocket = socket(AF_INET,SOCK_DGRAM)

# Doesn't know the name of the file yet!
reqFilename = ""

print("Binding...")
sSocket.bind(sAddr)
print("Ready for request.")

#Wait for client to request file.
request, cAddr = sSocket.recvfrom(100)
print("from %s: rec'd <%s>" % (repr(cAddr), repr(request)))
seqNumber, msgLen, reqFilename = request.decode().split(':')
print("SEQ:" + seqNumber)
# Open the file and send it to client line by line.
reqFile = open(reqFilename, "r")

ackn = "" #confirm acknowledge; this means the line got there!
status = "sending" #possible states: sending, sentMsg
tries = 0 #if tries == 3, exit program

line = reqFile.readline()

while line.strip() != "":
    line = str(seqNumber) + ":" + str(len(line.encode())) + ":" + line
    print ("Sending " + line)
    sSocket.sendto(line.encode(),cAddr)

    status = "sentMsg"
    ackn,addr = sSocket.recvfrom(100)
    ackn = ackn.decode()
        
    print("%s recieved." % ackn)
    status == "sending"
    line = reqFile.readline()
    seqNumber = int(seqNumber)
    seqNumber += 1

print("File sent. Sending end symbol...")
sSocket.sendto("#".encode(),cAddr)
status = "end"

        

    
