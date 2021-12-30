import socket
import time

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

while True: 

    msgFromClient       = input("Enter your message :")
    bytesToSend         = str.encode(msgFromClient +"1")
    serverAddressPort   = (get_ip_address(), 20001)
    bufferSize          = 1024

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)


    msg = "Message from Server :{}".format(msgFromServer[0].decode())

    print(msg)