import socket, traceback
from pymavlink import mavutil
from pathlib import Path
from datetime import datetime



def start_server():
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 33580
        s.bind(('', port))

        # not needed, will only handle one client .. kept for reference
        s.listen(5)
        print('Server is running on port '+ str(port))
        clientsocket, address = s.accept()
        print(f"Accepted connection from {address[0]}:{address[1]}")

        file = open_file("cuav_data", f"{address[0]}:{address[1]}")

        while True:
            received_message = clientsocket.recv(1024).decode("utf-8")
            if not received_message:
                print(f"connection probably closed by client")
                break
            print(received_message)
            file.write(f"{received_message}\n")
            file.flush()

            #byte_count = len(received_message.encode('utf-8'))
            #print(f"Number of bytes received: {byte_count}")
    except ConnectionResetError:
        # Handle unexpected client disconnection (connection reset by peer)
        print(f"Connection with {address[0]}:{address[1]} closed unexpectedly.")
        #file_cleanup(file.name)

    except Exception as e:
        print(traceback.format_exc())



def file_cleanup(filename):
    '''
    not needed, kept for reference - was used to cleanup empty lines in file. 
    '''
    
    '''
    with open('your_file.txt', 'r') as file:
        lines = file.readlines()

    # Remove trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    with open('your_file.txt', 'w') as file:
        file.writelines(lines)
    '''



def open_file(file_prefix, connection_details):
    data_folder = Path("data_received/")

    # check if 'data_received' folder exists, create it if not
    if not data_folder.is_dir():
        data_folder.mkdir()
    
    current_time = datetime.now()
    filename = current_time.strftime(f'{file_prefix}%d_%m_%Y__%H_%M_%S')
    file_to_open = data_folder / f"{filename}.txt"
    #file1 = open(f"{filename}.txt", "a")  # append mode
    file1 = open(file_to_open, "a")
    formatted_time = current_time.strftime('%d/%m/%Y - %H:%M:%S')
    file1.write(f"writing {file_prefix} from {connection_details} ---- {formatted_time}\n\n")
    file1.flush()
    return file1


if __name__ == "__main__":
    start_server()