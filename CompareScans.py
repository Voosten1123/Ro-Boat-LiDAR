from rplidar import RPLidar
from array import *
import sys
import matplotlib.pyplot as plt
lidar = RPLidar('/dev/ttyUSB0')

lidar.stop() #clears out buffer
here = 'here'
def get_scan():
    print('entry to get scan')
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
    print('exit from get scan')
    return arr

def process_scan(Matrix, RatioVariable, FlagNum):
    print('entry to process scan')
    i=0
    flag = 0
    flagBreak = 0

    spotslist = []

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
            #print("flag: ", "nodes:", Matrix[i][1] , Matrix[i+1][1] ,"| with Ratio: ", ratio, "| At ranges:", rangeB,rangeA)
        else:
            #print("flag break: ", "nodes:", Matrix[i][1] , Matrix[i+1][1] ,"| with Ratio: ", ratio, "| At ranges:", rangeB,rangeA)
            flagBreak = 1
            if flag > 0:
                print ("flag stop", flag)
            if flag > FlagNum:
                #--------------------------------------------------
                MeanQuality = (Matrix[i][0] + Matrix[i-flag][0])/2
                MeanAngle = (Matrix[i][1] + Matrix[i-flag][1])/2
                MeanDistance = (Matrix[i][2] + Matrix[i-flag][2])/2


                #--------------------------------------------------
                templ = [MeanQuality, MeanAngle, MeanDistance]
                #print('templ')
                #print(templ)
                spotslist.append(templ)
            templ = []
            flag = 0
        i += 1
    #print('exit from process scan')
    return spotslist

def compare_scans(scan1, scan2, anglethres, distthres):
    #print('entry to compare scans')
    i = 0
    j = 0
    Objectslist = []
    #print(here)
    while i < len(scan1):
        flag1 = 0
        flag2 = 0
        #print(here)
        while j < len(scan2):
            if abs(scan1[i][1] - scan2[j][1]) < anglethres:
                flag1 = 1
                #print(here)
                break
            if abs(scan1[i][2] - scan2[j][2]) < distthres:
                flag2 = 1
                #print(here)
                break
            j +=1
        if flag1 == 1 and flag2 == 1:
            templ = []
            templ = (scan2[j][0], scan2[j][1], scan2[j][2])
            Objectslist.append(templ)
            print(scan2[j][1], scan2[j][2], ' ', scan1[i][1], scan1[i][2])
            #print(here)
            break
        i += 1
    #print('exit from compare scans')
    return Objectslist













l = 0
while l < 5:

    datax = []
    datay = []
    dataz = []
    datax = process_scan(get_scan(), 0.1, 3)
    datay = process_scan(get_scan(), 0.1, 3)
    dataz = compare_scans(datax, datay, 5, 20)

    #data = process_scan(get_scan(), 0.1, 3)
    print('comparison')
    print('-----------------datax-------------------')
    print(datax)
    print('-----------------datay-------------------')
    print(datay)
    print('-----------------dataz-------------------')
    print(dataz)
    l +=1