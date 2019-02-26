#! /usr/bin/env python3
# A simple program implementing a server for a basic file transfer.

import sys
from socket import *
import sys, os, re, time

# The address and port of the server - socket, too
sAddr = ("",50000)
sSocket = socket(AF_INET, SOCK_DGRAM)

# Doesn't know the name of the file yet!
reqFilename = ""

print("Binding...")
sSocket.bind(sAddr)
print("Ready for request.")

#Wait for client to request file.
while reqFilename == "":
    request, cAddr = sSocket.recvfrom(100)
    print("from %s: rec'd <%s>" % (repr(cAddr), repr(request)))
    reqFilename = request.decode()

# Open the file and send it to client line by line.
reqFile = open(reqFilename, "r")
ack = "" #confirm acknowledge; this means the line got there!

for line in reqFile:
    sSocket.sendto(line.encode(), cAddr)
    print("Waiting for ACK.")
    #ack = sSocket.recvfrom(100)
    

sSocket.sendto(b'good', cAddr) # Let client know it's over!
print("File sent.")
