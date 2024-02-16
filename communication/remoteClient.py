import socket, traceback
from datetime import datetime
from threading import Timer
print ('hello')

port = 33580
host = '178.59.224.146'
s = socket.socket()

print ("default timeout: %s" %s.gettimeout())
s.settimeout(60)
print ("timeout now: %s" %s.gettimeout())

def background_controller():
    
    current_time = datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S')
    message = f"Hello server, my time is: {formatted_time}"
    print(f"sending server the time {formatted_time}")
    s.send(bytes(message, "utf-8"))
    #Timer(5, background_controller).start()
    
    
try:
    print("1")
    #s.bind(('', 33581))
    
    s.connect((host, port))
    print("2")
    #while True: 
    background_controller()

except Exception as e:
    print(traceback.format_exc())

'''
except Exception as e:
    print ("Couldnt connect with the socket-server: %s\n terminating program" + e)
    sys.exit(1)
'''	
