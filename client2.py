import socket
import time

while True: 

    msgFromClient       = input("Enter your message :")
    bytesToSend         = str.encode(msgFromClient +"2")
    serverAddressPort   = ("172.17.0.2", 20001)
    bufferSize          = 1024

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)


    msg = "Message from Server :{}".format(msgFromServer[0].decode())

    print(msg)