from numpy import random
from array import *

w, h = 2, 180
Matrix = [[0 for x in range(w)] for y in range(h)] 
i=0
while i<180:
    x = random.randint(11850)
    Matrix[i][0] = x
    y = random.randint(2000)
    Matrix[i][1] = y
    print("A", i, "R", Matrix[i][0], "S", Matrix[i][1])
    i += 1
print("end")

#//////////// first attempt /////////////////////////
#i=1
#RangeOne = Matrix[i][0]
#RangeTwo = Matrix[i-1][0]
#Dev1 = RangeOne-RangeTwo
#Dev2 = RangeTwo-RangeOne
#Ratio1 = RangeOne/Dev1
#Ratio2 = RangeTwo/Dev2
#Rsum = (Ratio1-Ratio2)/2 + Ratio1
#print(RangeOne,RangeTwo,Dev1,Dev2,Ratio1,Ratio2,Rsum)
#//////////////// second attempt /////////////
RatioVariable = 0.5
FlagNumber = 5
i=0
flag = 0
flagBreak = 0

ObjectsDetected = [0]

while i<180:
    rangeA = Matrix[i][0]
    rangeB = Matrix[i-1][0]
    if rangeA > rangeB:
        diff = rangeA-rangeB
        ratio = diff / rangeA
    else:
        diff = rangeB - rangeA
        ratio = diff / rangeB
    if ratio < RatioVariable:
        #print (ratio)
        flag += 1
        #print ("flag", flag)
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
    