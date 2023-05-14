from rplidar import RPLidar
from array import *
import sys
from time import time
lidar = RPLidar('/dev/ttyUSB0')

def get_scan():
    i = 0
    for scan in lidar.iter_scans():
        if i==1:
            break
        i+=1
    #scan is list of unknown length (scan outputs random number [ 80-120 measurements]). [i][j] i = individual measurement, j: 0 quality, 1 angle, 2 distance
    #print(arr[0][1])       #confirmation for test
    lidar.stop()
    return scan

def process_scan(Matrix, RatioVariable, FlagNum):
    #produces an array of measurements that are relatively close (ratiovariable/flagnumber control this) along with some derivative variables from said measurements.
    i=0
    flag = 0
    #used to mark and count "close" measurements
    spotslist = []
    #output array. spotslist[i][j]
    #i = number of spots. depends on flags
    #j = second array. 4 cells atm.
    #[i][0] = Mean Quality = Average quality (strength of signal) of the detected measurements (int 0-15, 15 perfect)
    #[i][1] = Mean Angle = the central angle of the detected  measurements (deg)
    #[i][2] = Mean Distance = the distance of the Mean Angle measurement (mm)
    #[i][3] = Length = approximate true length of the measurement. (mm)
    templ = []
    #temp list to pass variables in output array.

    LMatrix = len(Matrix)
    #-------------------------------------------------------------
    while i<LMatrix-1: #runs for length of input array (get scan doesnt always send the same number of measurements)
        #-------------------------------------------------------------
        rangeA = Matrix[i][2]
        rangeB = Matrix[i+1][2]
        #-------------------------------------------------------------
        if rangeA > rangeB:
            diff = rangeA-rangeB
            if diff == 0:
                diff = 1
            ratio = diff / rangeA
        #Ratio takes the difference between two consecutive measurements, and it divides the largest distance.
        #Largest distance so the ratio is smaller to get accurate measurements
        #-------------------------------------------------------------
        else:
            diff = rangeB - rangeA
            if diff == 0:
                diff = 1
            ratio = diff / rangeB
        #same as above
        #-------------------------------------------------------------
        if ratio < RatioVariable and Matrix[i+1][1] - Matrix[i][1] < 5:
            #if the ratio between measurements is within the threshold, they're flagged.
            #AND operator checks so the measurements are in "close" angles, and not just consecutive measurements
            flag += 1
            #templ.append(Matrix[i][1])
        else:
            #if ratio is larger than the threshold, then the two points are not close.
            #the spotted item will be now checked.
            #--------------------------------------
            if flag > FlagNum:
                #if number of close measurements is above the threshold, then it can be labelled a spot.
                #--------------------------------------------------
                #MeanQuality = (Matrix[i][0] + Matrix[i-flag][0])/2
                #MeanAngle = (Matrix[i][1] + Matrix[i-flag][1])/2
                #MeanDistance = (Matrix[i][2] + Matrix[i-flag][2])/2
                #--------------------------------------------------
                #MQ  = Mean Quality
                j = 0
                sum = 0
                while j <= flag:
                    sum = sum + Matrix[i-j][0]
                    j += 1
                MQ = sum/flag
                #runs backwards from ending measurement, and finds the average of all the qualities.
                #---------------------------------------------------
                #MD = Mean Distance
                sum = 0
                j = 0
                while j <= flag:
                    sum = sum + Matrix[i-j][2]
                    j += 1
                MD = sum/flag
                #same as above, but this time with distance
                #---------------------------------------------------
                #MA = Mean Angle
                angle = i - (flag%2)
                MA = Matrix[angle][1]
                #mean angle is the angle at half the measurements.
                #--------------------------------------------------
                #ML = Mean Length
                deg = 0 #how big the angle is between the ending angle and the starting one
                deg = Matrix[i][1] - Matrix[i-flag][1]
                if deg < 0:
                    #if the angles inclue 360/000, then the result will be negative as lets say, 010-352 = -342 degrees.
                    #if that happens, we add 360 to ensure its the correct number
                    deg = deg +360
                ML = deg * MD * 0.01745 # arc length on a circle circumference is θ * 1/360 * 2 * pi * ρ. 2pi /360 is 0.01745
                #θ = deg, MD = ρ (approximate)
                #--------------------------------------------------
                templ.append(MQ)
                templ.append(MA)
                templ.append(MD)
                templ.append(ML)
                #adds the variables to templ
                spotslist.append(templ)
                #adds the templ tuple to the output array
            templ = [] #empties templ
            flag = 0 #resets flag
        i += 1
    return spotslist

def Compare_Scans(Scan1, Scan2, QualityThres, AngleThres, DistThres, LengthThres):
    #takes two (maybe three in Ver3) scans, along with thresholds for: Quality, Angle, Distance, Length.
    #outputs an array of all objects that are within the thresholds (it outputs the latter scan as it was)
    #output to be fed into it as Scan1 with Scan2 being a fresh ProcessScan to update.
    i = 0
    #iterator for Scan1
    Objectslist = []
    #output list, same as scan
    while i < len(Scan1):
        flagQ = False
        flagA = False
        flagD = False
        flagL = False
        #flags for each threshold, capital letter indicating which one. Quality, Angle, Distance, Length
        j = 0
        #Iterator for Scan2
        while j < len(Scan2):
            #embedded loops so each item of Scan1 is checked with each item of Scan2
            if abs(Scan1[i][0] - Scan2[j][0]) < QualityThres:
                flagQ = True
            if abs(Scan1[i][1] - Scan2[j][1]) < AngleThres:
                flagA = True
            if abs(Scan1[i][2] - Scan2[j][2]) < DistThres:
                flagD = True
            if abs(Scan1[i][3] - Scan2[j][3]) < LengthThres:
                flagL = True
            if flagQ and flagA and flagD and flagL: #not sure if it must be AND for all. could do OR or XOR or smth
                templ = []
                #templ.append(Scan1[i])
                #templ.append(Scan2[j])
                #Objectslist.append(templ)
                Objectslist.append(Scan2[j])
                templ = []
                #print(Scan2[j][1], Scan2[j][2], ' ', Scan1[i][1], Scan1[i][2])
                break
            j +=1
        i += 1
    return Objectslist

lidar.reset()

while True:
    data1 = process_scan(get_scan(), 1.5, 3)
    data2 = process_scan(get_scan(), 1.5, 3)
    dataold = Compare_Scans(data1, data2, 3, 15, 120, 150)
    il = 0
    print('----------------------------')
    while il < len(dataold):
        #print('Id : ', il+1,  ' | Quality:', dataold[il][1][0], ' | Angle:', dataold[il][1][1],' | Distance:', dataold[il][1][2],' | Length:', dataold[il][1][3])
        #print('Id : ', il+1,  ' | Quality:', dataold[il][0], ' | Angle:', dataold[il][1],' | Distance:', dataold[il][2],' | Length:', dataold[il][3])
        if dataold[il][1] < 90:
            output = (dataold[il][1]) // 30
            print(output+1)
        elif dataold[il][1] > 270:
            output = (360-dataold[il][1]) // 30
            print(360-dataold[il][1])
            print(-output)
        else:
            print('poo')
        il +=1
    #print(dataz)
















