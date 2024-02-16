import socket, traceback, time
from datetime import datetime

print ('hello')

try:
    
    port = 33581
    host = '192.168.1.3'
    
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket()
    print ("default timeout: %s" %s.gettimeout())
    s.settimeout(60)
    print ("timeout now: %s" %s.gettimeout())
    #s.bind(('', 33581))
    s.connect((host, port))
    
    #current_time = datetime.now()
    #formatted_time = current_time.strftime('%H:%M:%S')
    #message = f"Hello server, my time is: {formatted_time}" 
    #print(message)
    
    
    while True:
        current_time = datetime.now()
        formatted_time = current_time.strftime('%H:%M:%S')
        message = f"Hello server, my time is: {formatted_time}" 
        print(f"sending {formatted_time} to server")
        s.send(bytes(message, "utf-8"))
        time.sleep(3)
        
        
except Exception as e:
    print(traceback.format_exc())
