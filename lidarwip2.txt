from numpy import random
from array import *

w, h = 2, 240
Matrix = [[0 for x in range(w)] for y in range(h)] 
i=0
while i<240:
    x = random.randint(11850)
    Matrix[i][0] = x
    y = random.randint(2000)
    Matrix[i][1] = y
    print("A", i, "R", Matrix[i][0], "S", Matrix[i][1])
    i += 1
Matrix[100][0] = 5600
Matrix[101][0] = 5601
Matrix[102][0] = 5602
Matrix[103][0] = 5603
Matrix[104][0] = 5604
Matrix[105][0] = 5605
print("end of array")

#//////////////// third attempt /////////////
RatioVariable = 0.015
FlagNumber = 5
i=1
flag = 0
flagBreak = 0

ObjectsDetected = [0]

while i<240:
    rangeA = Matrix[i][0]
    rangeB = Matrix[i-1][0]
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
    if ratio < RatioVariable:
        #print (ratio)
        flag += 1
        #print ("flag", flag)
        print("flag: ", "nodes:",i-1 ,i ,"| with Ratio: ", ratio, "| At ranges:", rangeB,rangeA)
    else:
        #print (ratio)
        flagBreak = 1
        if flag > 0:
            print ("flag stop", flag)
        if flag > FlagNumber:
            ObjectsDetected.append(i-flag)
        flag = 0
    i += 1
for j in ObjectsDetected:
    print(j)