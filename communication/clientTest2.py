import socket, traceback
print ('hello')

try:
    
    port = 33580
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("default timeout: %s" %s.gettimeout())
    s.settimeout(60)
    print ("timeout now: %s" %s.gettimeout())
    print("1")
    s.bind(('', 33581))
    s.connect(("192.168.2.6", port))
    #s.connect(("178.59.224.146", port))
    print("2")
    while True:
        print(s.recv(1024).decode("utf-8"))

except Exception as e:
    print(traceback.format_exc())

'''
except Exception as e:
    print ("Couldnt connect with the socket-server: %s\n terminating program" + e)
    sys.exit(1)
'''	
