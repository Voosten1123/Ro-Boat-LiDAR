import math


import matplotlib.pyplot as plt 
import matplotlib.transforms as mtransforms 
#import numpy as np 
from matplotlib.transforms import offset_copy 

pi = math.pi

#import matplotlib.pyplot as plt
#import numpy as np


def FindCPA2 (ID, Course, Bearing1, Range1, Time1, Bearing2, Range2, Time2):
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



def FormTriangleAngle(AngleA, AngleB, AngleC):
    if (AngleA+AngleB+AngleC) == 180:
        return True
    elif (AngleA+AngleB+AngleC) > 179 and (AngleA+AngleB+AngleC) < 181:
        return True
    else:
        return False


def bearing_to_cartesian(bearing_deg, range):
    """
    Convert a bearing and range to Cartesian coordinates.

    Parameters:
    bearing_deg (float): Bearing in degrees from the north, moving clockwise.
    range (float): Range in nautical miles.

    Returns:
    tuple: A tuple (x, y) of Cartesian coordinates.
    """
    bearing_rad = math.radians(bearing_deg)
    y = range * math.cos(bearing_rad)
    x = range * math.sin(bearing_rad)
    return x, y


def FindCPA3 (ID, Course, Bearing1D, Range1, Time1, Bearing2D, Range2, Time2):
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
    pi = 3.14159265358979323846

    #Absolute difference between the two Bearings
    DifferenceBetweenBearingsD = abs(Bearing1D-Bearing2D)

    #if the angle is larger than 180 degrees, then its the wrong side of the angle, so we get the complementary
    if DifferenceBetweenBearingsD > 180:
        DifferenceBetweenBearingsD = 360 - DifferenceBetweenBearingsD
    
    #Turning the angle to Radians
    DifferenceBetweenBearingsR = math.radians(abs(DifferenceBetweenBearingsD))      

    #Distance it has covered from Det 1 to Det 2 (using cosine rule)
    DistanceCovered = math.sqrt(Range1**2 + Range2**2 - 2*Range2*Range1*math.cos(DifferenceBetweenBearingsR))      

    #Target's Relative Motion Speed
    TargetRMS = DistanceCovered / (Time2-Time1)         

    #triangle semiperimeter
    sigma = (Range1 + Range2 + DistanceCovered)/2

    #Distance of CPA, through Heron's forumla and the triangle semiperimeter
    CPADistance = 2/DistanceCovered * math.sqrt(sigma*(sigma-Range1)*(sigma-Range2)*(sigma-DistanceCovered))

    #find the remaining 2 angles within triangle through cosine rules
    Range1Angle = math.acos((Range2**2 + DistanceCovered**2 - Range1**2) / (2 * Range2 * DistanceCovered))
    Range2Angle = math.acos((Range1**2 + DistanceCovered**2 - Range2**2) / (2 * Range1 * DistanceCovered))
    
    #convert from rad to deg
    R1Angle = math.degrees(Range1Angle)
    R2Angle = math.degrees(Range2Angle)
    
    #sanity printouts
    TotalAngles = R1Angle + R2Angle + DifferenceBetweenBearingsD
    print("Angle Between Points: "+ str(DifferenceBetweenBearingsD))
    print("Angle Opposite of R1: "+ str(R1Angle))
    print("Angle Opposite of R2: "+ str(R2Angle))
    print(TotalAngles)

    print("===================")
    print("CPA Distance: " + str(CPADistance) + " || Range1 : "+ str(Range1) + " || Range2 : "+str(Range2))

    if CPADistance < Range1 and CPADistance < Range2:
        #Then the Altitude [CPA Distance] of the triangle is inside the base [Distance Covered]
        bearing = 90 - R1Angle
        if Bearing1D > 180:
            CPABearing = 360-Bearing1D-bearing
        else: 
            CPABearing = Bearing1D-bearing
        print("CPA Bearing: "+ str(CPABearing))
    elif CPADistance < Range1 and CPADistance > Range2:
        #then the Altitude [CPA Distance] is outside, on the Range 1 Side
        print()
    elif CPADistance > Range1 and CPADistance < Range2:
        #then the Altitude [CPA Distance] is outside, on the Range 2 Side
        print()


def FindCPA (ID, Course, Bearing1_deg, Range1, Time1, Bearing2_deg, Range2, Time2):

    Bearing1_rad = math.radians(Bearing1_deg)
    Bearing2_rad = math.radians(Bearing2_deg)

    time_interval = Time2 - Time1
    bearing_difference_deg = abs(Bearing1_deg - Bearing2_deg)
    bearing_difference_rad = math.radians(bearing_difference_deg)
    distance_passed = math.sqrt(Range1**2 + Range2**2 - 2*Range1*Range2*math.cos(bearing_difference_rad))
    relative_motion_speed = distance_passed / time_interval
    
    #triangle semiperimeter
    sigma = (Range1 + Range2 + distance_passed)/2
    
    CPADistance = 2/distance_passed * math.sqrt(sigma*(sigma-Range1)*(sigma-Range2)*(sigma-distance_passed))

    angle_det_1_rad = math.acos((Range2**2 + distance_passed**2 - Range1**2) / (2 * Range2 * distance_passed))
    angle_det_2_rad = math.acos((Range1**2 + distance_passed**2 - Range2**2) / (2 * Range1 * distance_passed))

    angle_det_1_deg = math.degrees(angle_det_1_rad)
    angle_det_2_deg = math.degrees(angle_det_2_rad)
    
    x1, y1 = bearing_to_cartesian(Bearing1_deg, Range1)
    x2, y2 = bearing_to_cartesian(Bearing2_deg, Range2)

    dx = x2 - x1
    dy = y2 - y1
    #if dx < 0 then we're moving to the left, if >0 then we're moving to the right
    #if dy < 0 then we're moving downwards, if >0 then we're moving upwards

    vx = dx/time_interval
    vy = dy/time_interval

    direction = math.degrees(math.atan(dx/dy))
    if dx < 0 or (direction < 0 and dx > 0):
        direction = direction + 180
    #TODO fix this so it outputs correct course

    target_RM_speed = math.sqrt(vx**2 + vy**2)


    if bearing_difference_deg < 90 and angle_det_1_deg < 90 and angle_det_2_deg < 90:
        #acute -> CPA is within the triangle (ie: we already passed it)
        print("acute")
    elif bearing_difference_deg > 90:
        #obtuse, but CPA is within the triangle
        print("obtuse but within")
    elif dx < 0:
        #obtuse, and we're moving to the left
        print("Obtuse, CPA is to the left")
    elif dx > 0:
        #obtuse, and we're moving to the right
        print("obtuse, CPA is to the right")
        
    else:
        print("cant find CPA bearing")

    print("bearing 1 deg: "+ str(Bearing1_deg))
    print("bearing 2 deg: "+ str(Bearing2_deg))
    print("bearing 1 rad: "+ str(math.cos(Bearing1_rad)))
    print("bearing 2 rad: "+ str(math.cos(Bearing2_rad)))
    

    print("right most detection: "+ str(max(math.cos(Bearing1_rad), math.cos(Bearing2_rad))))


    #printouts
    print("Time interval: " + str(time_interval))
    print("Bearing Difference: " + str(bearing_difference_deg))
    print("Distance Passed: " + str(distance_passed))
    print("Relative Motion Speed: " + str(relative_motion_speed))
    print("Target RM Speed: " + str(target_RM_speed))
    print("Direction: " + str(direction))
    print("dx, dy: " + str(dx) + str(dy))

#print("=======================================================================")


#variable declaration
b1 = 263
r1 = 20
t1 = 0
b2 = 253
r2 = 15
t2 = 2


FindCPA(0, 0, b1, r1, t1, b2, r2, t2)

#==============================================================
#plotting

# Angle In Radians
theta = [i/180*pi for i in  [b1,b2]]
# Radius
radius = [r1,r2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.scatter(theta,radius, c ='r')
plt.polar(theta,radius,marker='o')
#plt.axline([bearing1, range1], [bearing2, range2], color='r')
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_title("Graph Title here", va='bottom')
plt.show()
