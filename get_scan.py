from rplidar import RPLidar
from array import *
import sys
import time
lidar = RPLidar('/dev/ttyUSB0')

def get_scan():
    i = 0
    for scan in lidar.iter_scans():
        arr = scan            #list of unknown length (scan outputs random number [ 80-120 measurements]). [i][j] i = individual measurement, j: 0 quality, 1 angle, 2 distance
        #print(arr[0][1])       #confirmation for test
        if i == 0:
            i +=1
        else:
            break
    #print(arr)
    lidar.stop()
    return arr