from rplidar import RPlidar
import numpy as np
import sys
lidar = RPlidar('/dev/ttyUSB0') #kanei connect to lidar sto ras

lidar.connect() #gia na pairnei dedomena
lidar.start_motor() #sxedon panta ksekinaei me motor on, alla just in case
lidar.reset() #reset to idle state, kanei clear to buffer twn scans
#lidar.clear_input() #den doulevei
llist = [] #to list sto opoio pername ta data
for scan in lidar.iter_scans(): #no clue
    llist.append(np.array(scan))  #no clue
    print('here') #roadmark
    iter += 1  #testing purposes, na stamatei meta apo 10 samples
    if iter > 10: #testing purposes
        break
lidar.reset() #kanei ksana clear to buffer
i = 0
while i < 10:
    print(llist[i][1][2]) #llist[i][j][k]. i = ?????, j = scan, k = 0/quality/strength, 1=angle, 2=distance
    i +=1
lidar.stop() #stamataei ta samples, just in case