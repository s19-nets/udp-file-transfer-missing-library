#! /usr/bin/env python3
# A simple program implementing a server for a basic file transfer.

import sys
from socket import *
import sys, os, re, time

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
while reqFilename == "":
    request, cAddr = sSocket.recvfrom(100)
    print("from %s: rec'd <%s>" % (repr(cAddr), repr(request)))
    reqFilename = request.decode()

# Open the file and send it to client line by line.
reqFile = open(reqFilename, "r")

ackn = "" #confirm acknowledge; this means the line got there!
status = "sending" #possible states: sending, sentMsg
tries = 0 #if tries == 3, exit program

line = reqFile.readline()

while line.strip() != "":

    sSocket.sendto(line.encode(),cAddr)

    print("Segment sent. Waiting for acknowledgement...")

    status = "sentMsg"
    
    while status == "sentMsg":
        ackn,addr = sSocket.recvfrom(100)
        ackn = ackn.decode()
        if ackn == "ACKN": #wait for acknowledgement
            print("%s recieved." % ackn)
            status == "sending"
            break #if ACK recieved, break the loop
        time.sleep(5)
        if tries == 3:
            print("Connection failed. Exiting...")
            exit

        tries+=1
        print("Timeout. Resending...")
        sSocket.sendto(line.encode(),cAddr)

    line = reqFile.readline()

print("File sent. Sending end symbol...")
sSocket.sendto("#".encode(),cAddr)
status = "end"

#while status == "end":
    #sSocket.recvfrom(100)


        

    
