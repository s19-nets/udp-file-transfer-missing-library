#! /usr/bin/env python3
import sys
from socket import *
import sys, os, re

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

for line in reqFile:
    sSocket.sendto(line.encode(), cAddr)

sSocket.sendto(b'good', cAddr) # Let client know it's over!
print("File sent.")
