import socket, traceback, time, threading
from datetime import datetime
import concurrent.futures



def do_something(num):
    
    while True:
        print ("doing something")
        time.sleep(2)
        
    
def send_data(num):
    
    try:
        
        port = 33580
        #host = '178.59.224.146'
        host = '192.168.1.3'
        
        #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = socket.socket()
        print ("default timeout: %s" %s.gettimeout())
        s.settimeout(60)
        print ("timeout now: %s" %s.gettimeout())
        #s.bind(('', 33581))
        s.connect((host, port))
        
        while True:
            current_time = datetime.now()
            formatted_time = current_time.strftime('%H:%M:%S')
            message = f"Hello server, my time is: {formatted_time}" 
            print(f"sending {formatted_time} to server")
            s.send(bytes(message, "utf-8"))
            time.sleep(3)
            
            
    except Exception as e:
        print(traceback.format_exc())


if __name__ == "__main__":
    thread_one = threading.Thread(target=send_data, args=(1,))
    thread_two = threading.Thread(target=do_something, args=(2,))
    thread_one.start()
    thread_two.start()
    
