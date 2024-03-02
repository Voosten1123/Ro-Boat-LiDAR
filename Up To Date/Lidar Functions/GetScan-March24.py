'''
Get Scan

Somehow pulls data from the sensor and returns them in an array.
the library used was the only one that functioned, but its still weird with its data


'''
#Lidar libraries
from rplidar import RPLidar
from array import *


def get_scan():
    try:
        i = 0 
        for scan in lidar.iter_scans():
            arr = scan            #list of unknown length (scan outputs random number [ 80-120 measurements]). 
            if i == 0:            #[i][j] i = individual measurement, j: 0 quality, 1 angle, 2 distance  
                i +=1             
            else:          #taking the second measurement because the first is almost always erroneous
                break
        lidar.stop()    #clears out lidar buffer, allows function to be called again
        return arr
    except:
        print("get scan fail")