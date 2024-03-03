import socket, traceback, time, threading, random, wifi
from datetime import datetime
import concurrent.futures
from pathlib import Path
import subprocess

import dronekit #dont need all of it so check it out later
from pymavlink import mavutil


def connect_to_drone(serial_port):
    try:
        # Connect to the autopilot (CUAV V5+) over a serial port
        drone = mavutil.mavlink_connection(serial_port, baud=57600)
        print(f"Connected to drone on {serial_port}")

        return drone

    except Exception as e:
        print(f"Error connecting to drone: {e}")
        return None


# try to reboot drone programmatically.. get IDs from a heartbeat message
def reboot_drone(drone, system_id, component_id):
    
    reboot_command = mavutil.mavlink.MAV_CMD_PREFLIGHT_REBOOT_SHUTDOWN
    
    # Parameters for reboot (set parameter 1 to 1 for reboot)
    param1 = 1

    # Send COMMAND_LONG message to initiate reboot
    drone.mav.command_long_send(
        system_id,
        component_id,
        reboot_command,
        0,
        param1,  # Parameter 1 (1 for reboot, 2 for shutdown)
        0,      # Parameters 2-7 (not used)
        0,
        0, #component ID (?)
        0,
        0,
        0
    )
    print("Reboot command sent to the drone.")
    # Wait for the reboot command to be processed
    time.sleep(5)
    
def request_home_position(drone):
    try:
        # Request the home position
        drone.mav.command_long_send(
            drone.target_system,  # Target System ID
            drone.target_component,  # Target Component ID
            mavutil.mavlink.MAV_CMD_GET_HOME_POSITION,  # Command ID for requesting home position
            0,  # Confirmation
            0,  # Param1 (unused)
            0,  # Param2 (unused)
            0,  # Param3 (unused)
            0,  # Param4 (unused)
            0,  # Param5 (unused)
            0,  # Param6 (unused)
            0   # Param7 (unused)
        )

        # Wait for the HOME_POSITION message response
        msg = drone.recv_match(type='HOME_POSITION', blocking=True, timeout=5)
        if msg:
            print("Received HOME_POSITION message!")
            print("Latitude:", msg.latitude)
            print("Longitude:", msg.longitude)
            print("Altitude:", msg.altitude)

        else:
            print("No HOME_POSITION message received within the specified timeout.")

    except Exception as e:
        print(f"Error sending/receiving messages: {e}")
    
    
def set_home_position(drone, latitude, longitude):
    try:
        # Encode the SET_HOME_POSITION message
        msg = drone.mav.command_long_encode(
            1,  # System ID
            1,  # Component ID
            mavutil.mavlink.MAV_CMD_DO_SET_HOME,  # Command ID
            0,  # Confirmation
            0,  # Param1 (unused)
            0,  # Param2 (unused)
            0,  # Param3 (unused)
            0,  # Param4 (unused)
            latitude,  # Param5 (latitude)
            longitude,  # Param6 (longitude)
            0  # Param7 (altitude)
        )

        # Send the message
        drone.mav.send(msg)
        print("SET_HOME_POSITION message sent!")

    except Exception as e:
        print(f"Error sending SET_HOME_POSITION message: {e}")
    


# test test check if param exists - used in conjuction with another function that set arbitrary param
def check_param(drone):
    timeout = time.time() + 5  # 10 seconds timeout
    while time.time() < timeout:
        msg = drone.recv_match(type='PARAM_VALUE', blocking=True)
        print(f"current param value: {msg.param_value}")
        #if msg.param_id.decode() == param_id:
            #print(f"Received PARAM_VALUE message! Current value of {param_id}: {msg.param_value}")
        break    
    
    
def battery_check(drone):
    
    # Example using pymavlink to request and print BATTERY_STATUS message
    drone.mav.request_data_stream_send(
        drone.target_system, drone.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_EXTENDED_STATUS, 1, 1
    )

    while True:
        msg = drone.recv_match(type='BATTERY_STATUS', blocking=True)
        #the previous method will wait indefinately until a matching message is received.
        # you can include a timeout (in seconds) by following usage (if timeout is reached, None is returned)
        #msg = drone.recv_match(type='BATTERY_STATUS', blocking=True, timeout=10)
        if msg:
            print("pymavlink BATTERY_STATUS:")
            print("Voltage: %f V" % (msg.voltages[0] / 1000.0))
            print("Current: %f A" % msg.current_battery)
            print("Remaining Capacity: %d %%" % msg.battery_remaining)
            print("Current Consumed: %d mAh" % msg.current_consumed)
            #print("Battery Temperature: %d C" % msg.temperature) unknown, returns INT16_MAX
            
            break
        
def check_various(drone):
    try:
        vfr_hud_speed = round(drone.messages['VFR_HUD'].groundspeed, 3)
        heading = drone.messages['VFR_HUD'].heading
        print(f"vfr_hud_speed={vfr_hud_speed}m/s, heading={heading}")
    
    except Exception as e:
        print(f"Error {e}")


'''
def check_temperature(drone):
    try:
        temperature = drone.messages['HIGH_LATENCY2'].temperature_air
        print(f"air temp={temperature}")
    
    except Exception as e:
        print(f"Error {e}")
'''     
'''
def check_drone_temperature(drone):
    while True:
        msg = drone.recv_msg()

        if msg is not None and msg.get_type() == 'HIGH_LATENCY':
            # Extract temperature information from the message
            temperature = msg.temperature_air  

            # Print the temperature
            print(f"Autopilot Temperature: {temperature} degrees Celsius")

            # Print the temperature
            print(f"Autopilot Temperature: {temperature} degrees Celsius")
            sleep(2)
'''    

def gps_check(drone):
    try:
        lon = drone.messages['GPS_RAW_INT'].lon  # Note, you can access message fields as attributes!
        lat = drone.messages['GPS_RAW_INT'].lat
        gps_speed =  drone.messages['GPS_RAW_INT'].vel # see https://mavlink.io/en/messages/common.html, search 'GPS ground speed'
        timestamp = drone.time_since('GPS_RAW_INT')
        print(f"lat={lat}, lon={lon}, gps_speed: {gps_speed}cm/s")
    except:
        print('No GPS_RAW_INT message received')


    

def heartbeat_check(drone):
    try:
        print("Waiting for HEARTBEAT message...")
        drone.wait_heartbeat()

        print("Received HEARTBEAT message!")
        print("System ID:", drone.target_system)
        print("Component ID:", drone.target_component)

    except Exception as e:
        print(f"Error: {e}")
        
    

def request_everything(drone):
    
    drone.param_fetch_all()
    while True:
        msg = drone.recv_msg()
        if msg and msg.get_type() == 'PARAM_VALUE':
            print(f"Parameter {msg.param_id}: {msg.param_value}")
            time.sleep(0.2)
    
    
#limit amount of messages  
def request_everything2(drone, max_messages):
    # Set to store unique parameter IDs
    unique_parameter_ids = []
    
    message_count = 0
    
    try:
        # Request fetching all parameters
        drone.param_fetch_all()
        
        # Wait for some time to allow parameters to be received
        time.sleep(2)
        
        while message_count < max_messages:
            #print("in here0")
            time.sleep(0.1)
            msg = drone.recv_msg()
            
            if msg and msg.get_type() == 'PARAM_VALUE':
                #print("in here1")
                parameter_id = msg.param_id
                if parameter_id not in unique_parameter_ids:
                    #print("in here2")
                    # Print information about the unique parameter
                    print(f"Parameter {msg.param_id}: {msg.param_value}")

                    # Add the parameter ID to the set
                    #unique_parameter_ids.add(parameter_id)
                    
                    # Add the parameter ID to the list
                    unique_parameter_ids.append(parameter_id)

                    # Increment the message count
                    message_count += 1
                else:
                    print(f"seems that Parameter {msg.param_id}: {msg.param_value} was already received before")
        print(f"reached the end after {message_count} messages")
    except Exception as e:
        print(f"{e}")
        return None
    


def request_everything_only_once(drone):
    # Set to store unique parameter IDs
    unique_parameter_ids = []
    
    message_count = 0
    
    try:
        # Request fetching all parameters
        #drone.param_fetch_all()
        
        # Wait for some time to allow parameters to be received
        #time.sleep(2)
        
        while True:
            #print("in here0")
            time.sleep(0.1)
            msg = drone.recv_msg()
            
            if msg and msg.get_type() == 'PARAM_VALUE':
                #print("in here1")
                parameter_id = msg.param_id
                if parameter_id not in unique_parameter_ids:
                    #print("in here2")
                    # Print information about the unique parameter
                    print(f"{message_count} - Parameter {msg.param_id}: {msg.param_value}")

                    # Add the parameter ID to the set
                    #unique_parameter_ids.add(parameter_id)
                    
                    # Add the parameter ID to the list
                    unique_parameter_ids.append(parameter_id)

                    # Increment the message count
                    message_count += 1
                else:
                    print(f"seems that Parameter {msg.param_id}: {msg.param_value} was already received before")
                    print(f"so breaking, after {message_count} messages")
                    break
        print(f"reached the end after {message_count} messages")
    except Exception as e:
        print(f"{e}")
        return None


# doesn't work ... params always empty, need to check. 
def request_everything_only_once2(drone):
    # Request fetching all parameters
    drone.param_fetch_all()

    # Wait for some time to allow parameters to be received
    time.sleep(5)

    # Retrieve and print parameter values
    params = drone.params
    
    if not params:
        print("No parameters received.")
    else:
        # Print the length of the parameters dictionary
        print(f"Total number of parameters: {len(params)}")

        # Iterate over the parameter names and values and print them
        for param_name, param_value in params.items():
            print(f"Parameter: {param_name}, Value: {param_value}")
    
    

if __name__ == "__main__":
    
    serial_port = '/dev/ttyACM1'

    # Connect to the drone
    drone = connect_to_drone(serial_port)

    if drone:
        try:
            
            while True:
                time.sleep(3)
                #reboot_drone(drone, 1, 0)
                #break
                #heartbeat_check(drone)
                #battery_check(drone)
                #gps_check(drone)
                #check_various(drone)
                
                #check_param(drone)
                #set_home_position(drone, 37.463493, 24.916088)
                #request_home_position(drone)
                
                #request_everything(drone)
                #request_everything2(drone, 40)
                request_everything_only_once(drone)
                #check_temperature(drone)
                #break
            
        except KeyboardInterrupt:
            # Allow the user to exit the program with Ctrl+C
            pass

        finally:
            # Close the connection when done
            drone.close()
            print("Connection closed.")
            


    