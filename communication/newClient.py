import socket, traceback, time
from datetime import datetime

print ('hello')

try:
    
    port = 33580
    host = '192.168.2.6'
    
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = socket.socket()
    print ("default timeout: %s" %s.gettimeout())
    s.settimeout(60)
    print ("timeout now: %s" %s.gettimeout())
    print("1")
    #s.bind(('', 33581))
    s.connect((host, port))
    
    current_time = datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S')
    message = f"Hello server, my time is: {formatted_time}" 
    print(message)
    #time.sleep(5)
    #s.sendall(b"hello")
    #s.send(bytes(message, "utf-8"))
    #print("done")
    
    while True:
        s.send(bytes(message, "utf-8"))
        time.sleep(1)
        #print("in loop")
        current_time = datetime.now()
        formatted_time = current_time.strftime('%H:%M:%S')
        message = f"Hello server, my time is: {formatted_time}" 
        
    
    '''
    print("2")
    while True:
        print(s.recv(1024).decode("utf-8"))
    '''
except Exception as e:
    print(traceback.format_exc())

'''
except Exception as e:
    print ("Couldnt connect with the socket-server: %s\n terminating program" + e)
    sys.exit(1)
'''	
