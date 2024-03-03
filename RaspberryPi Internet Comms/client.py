import socket, traceback, time, threading, random, wifi
from datetime import datetime
import concurrent.futures
from pathlib import Path
import subprocess

import dronekit #dont need all of it so check it out later
from pymavlink import mavutil


# connect to CUAV using Dronekit.
def connect_to_cuav():
    
    try:
        #print("finding port")
        connection_string = '/dev/ttyACM1'
        print("attempting connection to CUAV")
        global vehicle
        vehicle = dronekit.connect(connection_string, wait_ready=True, baud=57600)
        print("connected to CUAV")
        
    
    except Exception as e:
        print(traceback.format_exc())


# find WiFis when running in WINDOWS PCs
def find_wifis_windows():
    file = open_file("wifi_data")
    while True:
        current_time = datetime.now()
        formatted_time = current_time.strftime('%H:%M:%S')
        r = subprocess.run(["netsh", "wlan", "show", "networks"], capture_output=True, text=True).stdout
        ls = r.split("\n")
        ssids = '\n'.join([k for k in ls if 'SSID' in k])

        file.write(f"\n{formatted_time}:\n{ssids}")
        file.flush()
        time.sleep(5)
        

# find wifis in LINUX PCs (Raspberry) and write file.       
def find_wifis_linux():
    
    file = open_file("wifi_data")
    while True:
        current_time = datetime.now()
        formatted_time = current_time.strftime('%H:%M:%S')
        networks = wifi.Cell.all('wlan0')
        for net in networks:
            wifi_data_line = f"{formatted_time}, SSID: {net.ssid}, Signal Strength: {net.signal}, encrypted: {net.encrypted}"
            #print(wifi_data_line)
            file.write(f"{wifi_data_line}\n")
            file.flush()
        time.sleep(5)

        
        


def open_file(file_prefix):
    """
    Creates (and returns) file under 'data' subdirectory.
    
    File is currently used to hold either CUAV or WiFi data.
    Works both in Linux and Windows as is (dont mind the / or \).
    Filename will be created using incoming param and append a formatted timestamp.
    
    Parameters:
    - file_prefix: suitable file_prefix for the filename, e.g. 'cuav_data'
    
    Returns:
    - file to write data
    """
    data_folder = Path("data/")
    
    # Check if the 'data' directory exists, create it if not
    if not data_folder.is_dir():
        data_folder.mkdir()
    
    
    current_time = datetime.now()
    filename = current_time.strftime(f'{file_prefix}%d_%m_%Y__%H_%M_%S')
    file_to_open = data_folder / f"{filename}.txt"
    
    file1 = open(file_to_open, "a")
    formatted_time = current_time.strftime('%d/%m/%Y - %H:%M:%S')
    
    # first line in file
    file1.write(f"writing {file_prefix} ---- {formatted_time}\n\n")
    file1.flush()
    
    return file1


### ---
### cuav related functions that use Dronekit and each one returns a specific string
### ---


def read_battery_voltage():
    '''
    Return voltage information as string.
    Uses Vehicle.battery object from Dronekit.
    '''
    batteryObject = vehicle.battery
    return f"{round(batteryObject.voltage, 2)}"
    
'''
current and level might not be supported. NOT USED currently, left for reference. 

from: https://dronekit-python.readthedocs.io/en/latest/automodule.html#dronekit.Vehicle.battery

current – Battery current, in 10 * milliamperes. None if the autopilot does not support current measurement.
level – Remaining battery energy. None if the autopilot cannot estimate the remaining battery
'''
def read_battery_current():
    '''
    Return current information as string.
    Uses Vehicle.battery object from Dronekit.
    '''
    batteryObject = vehicle.battery
    return f"{round(batteryObject.current, 2)}"


def read_battery_level():
    '''
    Return battery level information as string.
    Uses Vehicle.battery object from Dronekit.
    '''
    batteryObject = vehicle.battery
    return f"{round(batteryObject.level, 2)}"


def read_longitude():
    '''
    Return vehicle longitude value, rounded to 6 decimals
    '''
    return f"{round(vehicle.location.global_frame.lon, 6)}"
    
def read_latitude():
    '''
    Return vehicle latitude value, rounded to 6 decimals
    '''
    return f"{round(vehicle.location.global_frame.lat, 6)}"


def read_groundspeed():
    '''
    Return vehicle groundspeed in m/s
    '''
    return f"{round(vehicle.groundspeed, 2)}"

def read_heading():
    '''
    Return vehicle heading in degrees (0...360), North is 0. 
    '''
    return f"{vehicle.heading}"

    


def send_data(host, port):
    '''
    Tries to connect to given host:port, create a message containing cuav_data
    and send message every 2 seconds.  Currently also writes message to file locally. 
    '''
    try:
        
        print(f"attempting connection to server: {host}:{port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #print ("default timeout: %s" %s.gettimeout())
        #set timeout to 20 seconds
        s.settimeout(20)
        print("timeout now: %s" %s.gettimeout())
        #s.bind(('', 33581))
        s.connect((host, port))
        print(f"connection SUCCESSFUL on server {host}:{port}")
        file1 = open_file("cuav_data")
        
        while True:
            
            current_time = datetime.now()
            formatted_time = current_time.strftime('%H:%M:%S')
            # test battery current and level, not supported in all autopilots
            print(f"battery level: {read_battery_level()}")
            print(f"battery current: {read_battery_current()}")
            
            # create a message containing all info. Probably not efficient (function calling is expensive in python)
            message = f"voltage: {read_battery_voltage()}, lat: {read_latitude()}, lon: {read_longitude()}, speed: {read_groundspeed()}, heading: {read_heading()}, timestamp: {formatted_time}"
            print(message)
            s.send(bytes(message, "utf-8"))
            file1.write(f"{message}\n")
            file1.flush()
            time.sleep(2)
            
            
    except Exception as e:
        print(f"something's wrong with {host}:{port}. Exception is {e}")


if __name__ == "__main__":
    
    port = 33580
    #host = '176.92.127.20'
    host = '192.168.2.6'
    
    connect_to_cuav()
    
    thread_one = threading.Thread(target=send_data(host, port))
    thread_two = threading.Thread(target=find_wifis_linux)
    
    thread_one.start()
    thread_two.start()
    
    
