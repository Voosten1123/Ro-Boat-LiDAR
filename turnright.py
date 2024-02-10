import sys
import random
import math
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
    vehicle.commands.next =  vehicle.commands.next+1
    #print(vehicle.commands.next)
    print("current pos")
    print(vehicle.location.global_frame.lat)
    print("current mode")
    print(vehicle.mode)
    while True:
            print(vehicle.location.global_frame)
except:
        print("main fail")
