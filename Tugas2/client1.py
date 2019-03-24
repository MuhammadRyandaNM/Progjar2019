import socket
import os

SERVER_IP = "127.0.0.1"
SERVER_PORT = 9000

BUFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mypath ="./File_Client1/"

fp = None
fileName = None
received = 0

sock.sendto("REQ", (SERVER_IP, SERVER_PORT))
print "Request Sent"
while True:
    data, addr = sock.recvfrom(BUFSIZE)
    if data[:5] == "START":
        fileName = data[6:].replace(" ", "")
        received = 0
        completeName = os.path.join(mypath, fileName)
        fp = open(completeName, "wb+")
        print "Receiving " + fileName
    elif data[:3] == "END":
        print fileName + " Received"
        fp.close()
    elif data[:5] == "CLOSE":
        print "Terminating Connection"
        break
    else:
        
        fp.write(data)
        received += len(data)
        print "Receiving "+ str(received) +" bytes of data"
print "Request Finished"