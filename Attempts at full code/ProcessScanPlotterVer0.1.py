from rplidar import RPLidar
from array import *
import sys
import matplotlib.pyplot as plt
lidar = RPLidar('/dev/ttyUSB0')

here = 'here'

def get_scan():
    lidar.reset()
    i = 0
    for scan in lidar.iter_scans():
        arr = scan            #list of unknown length (scan outputs random number [ 80-120 measurements]). [i][j] i = individual measurement, j: 0 quality, 1 angle, 2 distance
        #print(arr[0][1])       #confirmation for test
        print(arr[0][1])
        if arr[0][1] < 5 or arr[0][1] > 355:    #ensures that output arr starts at 000 deg.
            break
    #print(arr)
    return arr

def stop_motor():
    lidar.stop()
    lidar.stop_motor()

def process_scan(Matrix, RatioVariable, FlagNum):
    i=0
    flag = 0
    flagBreak = 0

    ObjectsDetected = []

    templ = []

    LMatrix = len(Matrix)
    while i<LMatrix-1:
        rangeA = Matrix[i][2]
        #print(Matrix[i][0], Matrix[i][2], Matrix[i][2])
        rangeB = Matrix[i+1][2]
        #print(Matrix[i+1][0], Matrix[i+1][2], Matrix[i+1][2])
        if rangeA > rangeB:
            diff = rangeA-rangeB
            if diff == 0:
                diff = 1
            ratio = diff / rangeA
        else:
            diff = rangeB - rangeA
            if diff == 0:
                diff = 1
            ratio = diff / rangeB
        if ratio < RatioVariable and Matrix[i+1][1] - Matrix[i][1] < 5:
            flag += 1
            templ.append(Matrix[i][1])
            print("flag: ", "nodes:", Matrix[i][1] , Matrix[i+1][1] ,"| with Ratio: ", ratio, "| At ranges:", rangeB,rangeA)
        else:
            print("flag break: ", "nodes:", Matrix[i][1] , Matrix[i+1][1] ,"| with Ratio: ", ratio, "| At ranges:", rangeB,rangeA)
            flagBreak = 1
            if flag > 0:
                print ("flag stop", flag)
            if flag > FlagNum:
                #j = 0
                #while j < flag-i:
                #    templ.append(Matrix[j][1])
                templ.append(Matrix[i][1])
                ObjectsDetected.append(templ)
            templ = []
            flag = 0
        i += 1
    for j in ObjectsDetected:
        print(j)
    l = 0
    datx = []
    daty = []
    while l < LMatrix-1:
        datx.append(Matrix[l][1])
        daty.append(Matrix[l][2])
        #print(here)
        l += 1
    plt.plot(datx, daty, color = "red", marker = "o"),  # plotting by columns
    plt.show()
    #print(here)

process_scan(get_scan(), 0.1, 3)