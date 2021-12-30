import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
  
localIP     = get_ip_address()
localPort   = 20001
bufferSize  = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
 
UDPServerSocket.bind((localIP, localPort))

print("Server up and listening")

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
 
    m=message.decode()

    clientMsg = "Message from Client "+m[len(m)-1]+": "+m[0:len(m)-1]
    clientIP  = "Client IP Address: {}".format(address)
    
    print(clientMsg)

    msgFromServer       = input("Enter your message for client "+m[len(m)-1]+": ")
    bytesToSend         = str.encode(msgFromServer)

    UDPServerSocket.sendto(bytesToSend, address)