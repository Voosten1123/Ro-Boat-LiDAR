from rplidar import RPLidar
import numpy as np
import sys
lidar = RPLidar('/dev/ttyUSB0')

#lidar.connect()
#lidar.start_motor()
lidar.reset()
#lidar.motor_speed(60)  #dokimasa me integer
#lidar.motor_speed(12C) #dokimasa me hex, exei paraksena parameters, nmz einai ena parakseno format, b'\xF0'. ti einai? den kserw.
def get_scan():
    samples = []
    iter = 0
    for scan in lidar.iter_scans():
        print(scan)
        samples.append(np.array(scan))
        iter += 1
        #print('here')
        if iter >20:
            lidar.stop()
            break
get_scan()
print('end')