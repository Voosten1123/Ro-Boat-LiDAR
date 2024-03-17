import math

#import matplotlib.pyplot as plt
#import numpy as np


def FindCPA (ID, Course, Bearing1, Range1, Time1, Bearing2, Range2, Time2):
    pi = 3.14159265358979323846
    '''
    this function finds the Closest Point of Approach for 2 given detections.
    provide the boat's course (in degrees), the bearing, range, and time of 1st and 2nd detection.
    the function will print 4 things, CPA Bearing, CPA Range, CPA time, and CPA ETA each corresponding to:
    CPA Bearing: The angle at which we will be the closest to the target    [deg]
    CPA Range: The closest we'll ever get to the target                     [m]
    CPA Time: Time when the things above happen                             [s]
    CPA ETA: Time we have until CPA Time                                    [s]

    -------------------------------------------------------------------------------------------------------
    PS: I know its a lot of math, check the github repo for an attempt of making this into a graphic explanation.
    its 5AM, I cant explain trigonometry.
    '''
    #print("============================================================================================")
    AngleBetweenBearings = Bearing1 - Bearing2  #find angle between the points
    AngleBB = AngleBetweenBearings * (pi/180)   #convert to rads
    DistanceCovered = math.sqrt(Range1**2+ Range2**2 - 2*Range1*Range2*math.cos(AngleBB))  #cosine rule to find the relatve distance that the target traveled
    RMLtoBearing = math.asin((Range1*math.sin(AngleBB))/DistanceCovered)    #Sine rule to find relative motion line (RML) angle
    if RMLtoBearing > pi:                                                   #making sure its proper numbers
        RMLtoBearing = RMLtoBearing - pi
    #print("============================================================================================")
    CPADistance = Range2 * math.sin(RMLtoBearing)                           #Sine rule again, but this time to find the CPA distance
    DistanceToCover = math.sqrt(Range2**2-CPADistance**2)                   #Pythagorean Theorem to find distance between 2nd Detection and CPA
    PrimaryBearing = math.asin(DistanceToCover/Range2)                             #Sine rule to find angle from 2nd bearing
    CPABearing = math.radians(Bearing2) - PrimaryBearing                           #translating that to true bearing
    if CPABearing < 0:                                                      #formating (so it doesnt show -20 degrees, but instead 340)
        CPABearing = pi*2 + CPABearing 
    if CPABearing > 6.28:                                                   #formating again (20 degrees instead of 380)
        CPABearing = CPABearing -6.28
    TargetRMS = DistanceCovered / (Time2-Time1)                             #relative motion speed (RMS) is distance covered over time
    CPAEta = DistanceToCover/TargetRMS                                      #Time from 2nd detection till CPA
    CPATime = Time2+CPAEta                                                  #global time? TODO make it use native clock
    TargetRML = abs(math.degrees(Bearing2)) + abs(math.degrees(RMLtoBearing))       #RML angle
    if TargetRML < 0:
        while TargetRML < 360:
            TargetRML = TargetRML + 180
    if TargetRML > 360:
        while TargetRML > 360:
            TargetRML = TargetRML -180
    #print("============================================================================================")
    #passing params to object    
    #CPADistance
    #CPABearing
    #CPAEta
    #CPATime
    #TargetRMS
    #TargetRML 
    #returns
    print("Bearing1: "+ str(Bearing1) + "Range1: " + str(Range1) + "Bearing 2: "+ str(Bearing2) + "Range 2: " + str(Range2))
    print("CPA Bearing: "+ str(math.degrees(CPABearing)) + " || CPA Range: "+str(CPADistance)+ " || CPATime: "+str(CPATime)+ " || CPA ETA: "+ str(CPAEta)+ " || RML: "+str(TargetRML))
    print("Target RMS"+ str(TargetRMS))

FindCPA(0, 0, 30, 20, 0, 10, 15, 2)