import socket            
 
s = socket.socket()        
 
port = 12345               
 
s.connect(('192.168.65.140', port))
 
print (s.recv(1024).decode())
s.close()