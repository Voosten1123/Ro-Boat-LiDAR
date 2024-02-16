import sys
import random
import math
import time
#bridge libraries
import dronekit #dont need all of it so check it out later
from pymavlink import mavutil
print("finding port")
connection_string = '/dev/ttyACM0'
print("attempting connection")
vehicle = dronekit.connect(connection_string, wait_ready=True, baud=57600)
print("connected")
#bridge defs // big thanks to Saiffullah Sabir Mohamed from Elucidate drones for most of this < https://www.elucidatedrones.com/posts/how-to-control-drone-with-keyboard-using-dronekit-python/#code-explanation >
def send_to(latitude, longitude, altitude):
    try:
        '''
        This function will send the drone to desired location, when the 
        vehicle is in GUIDED mode.

        Inputs:
            1.  latitude            -   Destination location's Latitude
            2.  longitude           -   Destination location's Longitude
            3.  altitude            -   Vehicle's flight Altitude
        '''

        if vehicle.mode.name == "GUIDED":
            location = LocationGlobalRelative(latitude, longitude, float(altitude))
            vehicle.simple_goto(location)
            time.sleep(1)
    except:
        print("fail")

def destination_location(homeLattitude, homeLongitude, distance, bearing):
    try:
        '''
        This function returns the latitude and longitude of the
        destination location, when distance and bearing is provided.

        Inputs:
            1.  homeLattitude       -   Home or Current Location's  Latitude
            2.  homeLongitude       -   Home or Current Location's  Latitude
            3.  distance            -   Distance from the home location
            4.  bearing             -   Bearing angle from the home location
        '''

        #Radius of earth in metres
        R = 6371e3
        pie = math.pi
        rlat1 = homeLattitude * (pie/180) 
        rlon1 = homeLongitude * (pie/180)

        d = distance

        #Converting bearing to radians
        bearing = bearing * (pie/180)

        rlat2 = math.asin((math.sin(rlat1) * math.cos(d/R)) + (math.cos(rlat1) * math.sin(d/R) * math.cos(bearing)))
        rlon2 = rlon1 + math.atan2((math.sin(bearing) * math.sin(d/R) * math.cos(rlat1)) , (math.cos(d/R) - (math.sin(rlat1) * math.sin(rlat2))))

        #Converting to degrees
        rlat2 = rlat2 * (180/pie) 
        rlon2 = rlon2 * (180/pie)

        # Lat and Long as an Array
        location = [rlat2, rlon2]

        return location
    except:
        print("fail")

def snap_manuever(value):
    #aa = int(vehicle.heading)
    print(value)
    try:
        '''
        This function executes short turns 
        Input is a string that is used to define the manuever 
        W - left 90
        NW - left 45
        NNW - left 20
        NNE - right 20
        NE -  right 45
        E - right 90
        '''
        #ship current heading and location
        print('1here')
        #print(vehicle.wait_heartbeat)
        angle = int(vehicle.heading)
        print('2here')
        loc   = (vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_relative_frame.alt)
        print('3here')
        #distance per step, possibly interuptable. measured in meters
        default_distance = 5
        
        #configure heading 
        if value == 'W':
            print('here')
            NewBearing = angle - 90 
        elif value == 'NW':
            NewBearing = angle - 45 
        elif value == 'NNW':
            NewBearing = angle - 20
        elif value == 'NNE':
            NewBearing = angle + 20
        elif value == 'NE':
            NewBearing = angle + 45 
        elif value == 'E':
            NewBearing = angle + 90     
        
        #execute manuever
        new_loc = destination_location(homeLattitude = loc[0], homeLongitude = loc[1], distance = default_distance, bearing = NewBearing)
        send_to(new_loc[0], new_loc[1], loc[2])
    except:
        print("fail4")

def manuever(turn):
    try:
        vehicle.mode="GUIDED"
        #This function executes turns
        #ship current heading and location
        angle = int(vehicle.heading)
        loc   = (vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_relative_frame.alt)
        
        #distance per step, possibly interuptable. measured in meters
        default_distance = 5
        #execute manuever
        NewBearing = angle + turn
        new_loc = destination_location(homeLattitude = loc[0], homeLongitude = loc[1], distance = default_distance, bearing = NewBearing)
        send_to(new_loc[0], new_loc[1], loc[2])
        vehicle.mode="AUTO"
    except:
        print("fail")
        
def CurrLat():
    try:
        return vehicle.location.global_frame.lat
    except:
        print("fail")
def CurrLon():
    try:
        return vehicle.location.global_frame.lon
    except:
        print("fail")
def CurrGPS():
    try:
        return vehicle.location.global_frame
    except:
        print("fail")
        
try:
    print("here")
    #vehicle.commands.next =  vehicle.commands.next+1
    #print(vehicle.commands.next)
    #print("current pos")
    #print(vehicle.location.global_frame.lat)
    #print("current mode")
    #print(vehicle.mode)
    #'''
    print("\nGet all vehicle attribute values:")
    print(" Autopilot Firmware version: %s" % vehicle.version)
    print("   Major version number: %s" % vehicle.version.major)
    print("   Minor version number: %s" % vehicle.version.minor)
    print("   Patch version number: %s" % vehicle.version.patch)
    print("   Release type: %s" % vehicle.version.release_type())
    print("   Release version: %s" % vehicle.version.release_version())
    print("   Stable release?: %s" % vehicle.version.is_stable())
    print(" Autopilot capabilities")
    print("   Supports MISSION_FLOAT message type: %s" % vehicle.capabilities.mission_float)
    print("   Supports PARAM_FLOAT message type: %s" % vehicle.capabilities.param_float)
    print("   Supports MISSION_INT message type: %s" % vehicle.capabilities.mission_int)
    print("   Supports COMMAND_INT message type: %s" % vehicle.capabilities.command_int)
    print("   Supports PARAM_UNION message type: %s" % vehicle.capabilities.param_union)
    print("   Supports ftp for file transfers: %s" % vehicle.capabilities.ftp)
    print("   Supports commanding attitude offboard: %s" % vehicle.capabilities.set_attitude_target)
    print("   Supports commanding position and velocity targets in local NED frame: %s" % vehicle.capabilities.set_attitude_target_local_ned)
    print("   Supports set position + velocity targets in global scaled integers: %s" % vehicle.capabilities.set_altitude_target_global_int)
    print("   Supports terrain protocol / data handling: %s" % vehicle.capabilities.terrain)
    print("   Supports direct actuator control: %s" % vehicle.capabilities.set_actuator_target)
    print("   Supports the flight termination command: %s" % vehicle.capabilities.flight_termination)
    print("   Supports mission_float message type: %s" % vehicle.capabilities.mission_float)
    print("   Supports onboard compass calibration: %s" % vehicle.capabilities.compass_calibration)
    print(" Global Location: %s" % vehicle.location.global_frame)
    print(" Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
    print(" Local Location: %s" % vehicle.location.local_frame)
    print(" Attitude: %s" % vehicle.attitude)
    print(" Velocity: %s" % vehicle.velocity)
    print(" GPS: %s" % vehicle.gps_0)
    print(" Gimbal status: %s" % vehicle.gimbal)
    print(" Battery: %s" % vehicle.battery)
    print(" EKF OK?: %s" % vehicle.ekf_ok)
    print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
    print(" Rangefinder: %s" % vehicle.rangefinder)
    print(" Rangefinder distance: %s" % vehicle.rangefinder.distance)
    print(" Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
    print(" Heading: %s" % vehicle.heading)
    print(" Is Armable?: %s" % vehicle.is_armable)
    print(" System status: %s" % vehicle.system_status.state)
    print(" Groundspeed: %s" % vehicle.groundspeed)    # settable
    print(" Airspeed: %s" % vehicle.airspeed)    # settable
    print(" Mode: %s" % vehicle.mode.name)    # settable
    print(" Armed: %s" % vehicle.armed)    # settable
        #'''
    
    
    while False:
            print(vehicle.mode)
            #vehicle.mode = "GUIDED"
            #print(vehicle.mode)
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(current_time)
            time.sleep(5)
except:
        print("main fail")
