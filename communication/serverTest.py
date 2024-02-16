import socket
import time

from threading import Timer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 33580
s.bind(('', port))
s.listen(5)
print('Server is running on port '+ str(port))
counter = 1

def background_controller():
    message = "Hello client "
    print(message)
    clientsocket.send(bytes(message, "utf-8"))
    Timer(5, background_controller).start()

while True:
    #counter+=1
    clientsocket, address = s.accept()
    #print(f"Connection from {address} has been established")
    print(f"Accepted connection from {address[0]}:{address[1]}")
    background_controller()




