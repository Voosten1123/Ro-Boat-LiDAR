from rplidar import RPLidar
from array import *
import sys
lidar = RPLidar('/dev/ttyUSB0')

lidar.reset() #clears out buffer
here = 'here'
def get_scan():
    i = 0
    for scan in lidar.iter_scans():
        arr = scan            #list of unknown length (scan outputs random number [ 80-120 measurements]). [i][j] i = individual measurement, j: 0 quality, 1 angle, 2 distance
        print(arr[0][1])       #confirmation for test
        if arr[0][1] < 1 or arr[0][1] > 360:    #ensures that output arr starts at 000 deg.
            break
    print(arr)
    return arr

get_scan()