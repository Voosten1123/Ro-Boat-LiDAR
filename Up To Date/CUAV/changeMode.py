"""
Example of how to change flight modes using pymavlink

from code found here: https://www.ardusub.com/developers/pymavlink.html ..

alternative methods of changing mode though didn't seem to work ... 
"""

import sys, traceback
# Import mavutil
from pymavlink import mavutil

def connect_to_cuav():
    serial_port = '/dev/cuav'
    
    try:
    
        # Create the connection
        drone = mavutil.mavlink_connection(serial_port, baud=57600)
        # Wait a heartbeat before sending commands
        drone.wait_heartbeat()
        print("drone connected ok")
        return drone
    
    except Exception as e:
        # Print the exception message
        print(f"ohoh Exception: {str(e)}")
        # Use the traceback module to print the stack trace
        traceback.print_exc()


def check_current_mode(drone):
    try:
        while True:
            msg = drone.recv_match(type='HEARTBEAT', blocking=True)
            mode = mavutil.mode_string_v10(msg)
            mode_id = drone.mode_mapping()[mode]
            print(f"current mode: {mode}, with id: {mode_id}")
            break
    except Exception as e:
        # Print the exception message
        print(f"Exception: {str(e)}")
        traceback.print_exc()


def change_mode(drone, new_mode):

    # Check if mode is available
    if new_mode not in drone.mode_mapping():
        print('Unknown mode : {}'.format(mode))
        print('Try:', list(drone.mode_mapping().keys()))
        sys.exit(1)
    
    try:
        new_mode_id = drone.mode_mapping()[new_mode]
        print(f"changing mode to: {new_mode}, with id: {new_mode_id}")
        
        drone.set_mode(new_mode_id)
        
        while True:
            print("waiting for ACK")
            # Wait for ACK command
            # Would be good to add mechanism to avoid endlessly blocking
            # if the autopilot sends a NACK or never receives the message
            ack_msg = drone.recv_match(type='COMMAND_ACK', blocking=True)
            ack_msg = ack_msg.to_dict()

            # Continue waiting if the acknowledged command is not `set_mode`
            if ack_msg['command'] != mavutil.mavlink.MAV_CMD_DO_SET_MODE:
                continue

            # Print the ACK result !
            print(f"received ACK: {mavutil.mavlink.enums['MAV_RESULT'][ack_msg['result']].description}")
            #print("RECEIVED ACK, check message above")
            break
        
    except Exception as e:
        # Print the exception message
        print(f"Exception: {str(e)}")

        # Use the traceback module to print the stack trace
        traceback.print_exc()
        


if __name__ == "__main__":
    
    
    drone = connect_to_cuav()
    print("simple program to change mode.. ")
    print("available modes seem to be: ")
    print(list(drone.mode_mapping().keys()))
    
    check_current_mode(drone)
    change_mode(drone, 'RTL')
    check_current_mode(drone)
    
    
    