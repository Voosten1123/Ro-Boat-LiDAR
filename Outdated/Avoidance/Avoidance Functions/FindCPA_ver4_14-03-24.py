import math


import matplotlib.pyplot as plt 
import matplotlib.transforms as mtransforms 
#import numpy as np 
from matplotlib.transforms import offset_copy 

pi = 3.14159265358979323846
CPB = 0
CPD = 0

#import matplotlib.pyplot as plt
#import numpy as np

#Outdated versions of CPA ====================
def FindCPA2 (ID, Course, Bearing1, Range1, Time1, Bearing2, Range2, Time2):
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

def FindCPA4 (ID, Course, Bearing1_deg, Range1, Time1, Bearing2_deg, Range2, Time2):

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

def FindCPA5 (Bearing1_deg, Range1, Time1, Bearing2_deg, Range2, Time2):
    if Range2 < Range1: 
        #find interim angle
        InterAngle = FindInterim(Bearing1_deg, Bearing2_deg)

        #form triangle to get the remaining data on triangle
        Triangle = FindWrongAngle(InterAngle, Range1, Range2)
        #print(Range1, Range2)
        #print(Triangle[0])
        
        #if triangle is proper
        if Triangle[0] != -1:
            #Assign the angles to variables   
            Bearing1_angle = Triangle[1]
            Bearing2_angle = Triangle[2]

            #supplementary angles
            Bearing1_suppl = 180 - Bearing1_angle
            Bearing2_suppl = 180 - Bearing2_angle
        else:
            return -1


        #make the bearings into cartesians
        x1, y1 = bearing_to_cartesian(Bearing1_deg, Range1)
        x2, y2 = bearing_to_cartesian(Bearing2_deg, Range2)
        #print(x1, y1)
        #print(x2, y2)

        #produce movement vector
        dx = x2 - x1
        dy = y2 - y1
        print(dx, dy)

        #distance covered 
        distance_covered = math.sqrt(dx*dx +dy*dy)


        #find direction of movement
        direction = '0'
        if dx > 0 and dy > 0:
            direction = 'NE'
            print("NE")
        if dx > 0 and dy < 0:
            direction = 'SE'
            print("SE")
        if dx < 0 and dy < 0:
            direction = 'SW'
            print("SW")
        if dx < 0 and dy > 0:
            direction = 'NW'
            print("NW")

        if direction == "NE" or direction == "SE":
            print("going left")
            #use the rightmost angle in this case 
            
            #finding which bearing is rightmost
            if Range1 > Range2:
                #bearing 1 is right most

                #Pythagorean theorem to find CPA distance
                #CPA_distance = Range1*math.sin(math.radians(Bearing1_angle))
                CPA_distance = Range1*math.sin(math.radians(Bearing1_suppl))
                
                #sine rule to find the remaining distance to cover
                #distance_to_cover = math.sqrt(Range1*Range1-CPA_distance*CPA_distance)-distance_covered
                distance_to_cover = math.sqrt(Range1*Range1-CPA_distance*CPA_distance)
                
                #sine rule to find the total angle between bearing 1 and CPA bearing
                #InitBearing = math.asin(((distance_to_cover+distance_covered)*math.sin(math.radians(Bearing1_angle)))/CPA_distance)
                InitBearing = 90 - Bearing2_suppl

                #finding the proper CPA bearing (degrees)
                #CPA_Bearing = Bearing1_deg - math.degrees(InitBearing)
                CPA_Bearing = Bearing1_deg + InitBearing
            else:
                #CPA_distance = Range2*math.sin(math.radians(Bearing2_angle))
                CPA_distance = Range2*math.sin(math.radians(Bearing2_suppl))
                #distance_to_cover = math.sqrt(Range2*Range2-CPA_distance*CPA_distance)-distance_covered
                distance_to_cover = math.sqrt(Range2**2- CPA_distance**2)
                #InitBearing = math.asin(((distance_to_cover+distance_covered)*math.sin(math.radians(Bearing2_angle)))/CPA_distance)
                InitBearing = 90 - Bearing1_suppl
                #CPA_Bearing = Bearing2_deg - math.degrees(InitBearing)
                CPA_Bearing = Bearing2_deg + InitBearing
        else:
            print("going right")
            #use the leftmost angle in this case 
            if Range1 < Range2:
                CPA_distance = Range1*math.sin(math.radians(Bearing1_suppl))
                distance_to_cover = math.sqrt(Range1*Range1-CPA_distance*CPA_distance)
                #InitBearing = math.asin(((distance_to_cover+distance_covered)*math.sin(math.radians(Bearing1_angle)))/CPA_distance)
                InitBearing = 90 - Bearing2_suppl
                #CPA_Bearing = Bearing1_deg - math.degrees(InitBearing)
                CPA_Bearing = Bearing1_deg + InitBearing
            else:
                CPA_distance = Range2*math.sin(math.radians(Bearing2_suppl))
                distance_to_cover = math.sqrt(Range2**2- CPA_distance**2)
                #InitBearing = math.asin(((distance_to_cover+distance_covered)*math.sin(math.radians(Bearing2_angle)))/CPA_distance)
                InitBearing = 90 - Bearing1_suppl
                CPA_Bearing = Bearing2_deg + InitBearing 
              
        
        #correcting for negative 
        if CPA_Bearing < 0:
            print("correcting CPA Bearing -")
            while CPA_Bearing < 360:
                CPA_Bearing = 360 + CPA_Bearing
        
        #correcting for over positive
        if CPA_Bearing > 360:
            print("correcting CPA Bearing+")
            while CPA_Bearing > 360:
                CPA_Bearing = CPA_Bearing - 360
        
        target_RMS = distance_covered/(Time2-Time1)
        CPA_Eta = distance_to_cover / target_RMS
        CPA_Time = CPA_Eta + Time2
        
        #====
        print("CPA_Bearing = "+ str(CPA_Bearing))
        print("CPA_Distance = "+ str(CPA_distance))
        if CPA_Eta < 0:
            print("CPA is in the past")
            print("CPA_Time = "+ str(CPA_Time))
        else:    
            print("CPA_ETA = "+ str(CPA_Eta))
            print("CPA_Time = "+ str(CPA_Time))
        print("Target RMS = "+ str(target_RMS))
        
    else:
        print("CPA is in the past")


#=============================================
    
def FindWrongAngle(AngleA, SideB, SideC):
    '''
    takes an angle and 2 sides.
    returns:
        [-1] = error
        [0] = no wrong angles
        [1] = angle B is wrong
        [2] = angle C is wrong
    along with both angles
    '''
    Adeg = AngleA   #name consistency

    #cosine rule to find side opposite of angle A
    SideA = CosineRule(SideB, SideC, Adeg)

    #sine rule to find angles B and C (in rad)
    Brad = math.asin((SideB*math.sin(math.radians(Adeg)))/SideA)
    Crad = math.asin((SideC*math.sin(math.radians(Adeg)))/SideA)

    #convert to degrees
    Bdeg = math.degrees(Brad)
    Cdeg = math.degrees(Crad)

    #angle sum
    ABCtot = Adeg + Bdeg + Cdeg

    '''
    if B or C are obtuse (more than 90 deg), Bdeg/Cdeg will be wrong
    they're going to be the supplementary of the angle we're looking for
    (supplementary is the angle with which a perfect line is drawn)
    so to find the correct angle, we remove the angle from 180
    '''
    if round(ABCtot) != 180:
        
        #making the alternative angles
        Bdeg_alt = 180 - Bdeg
        Cdeg_alt = 180 - Cdeg

        #making the two alternative totals
        ABCB = Adeg + Bdeg_alt + Cdeg
        ABCC = Adeg + Bdeg + Cdeg_alt
        #(not possible for two angles to be obtuse in the same triangle)
        if round(ABCB) == 180:      #if B is wrong
            Bdeg = Bdeg_alt         #change B to the alternative
            print("====\nchanged B\n====")
            return 1, Bdeg, Cdeg
        elif round(ABCC) == 180:    #if C is wrong
            Cdeg = Cdeg_alt         #change C to the alternative
            print("====\nchanged C\n====")
            return 2, Bdeg, Cdeg
        else:
            print("failed to make a triangle")      #safety
            print("Angle A : " + str(Adeg)+ " || Angle B : " + str(Bdeg)+ " || Angle C : " + str(Cdeg)) #for checking
            return -1, -2, -2
    return 0, Bdeg, Cdeg

def FindInterim (angle1, angle2):
    '''
    takes 2 angles (deg) and returns the angle (deg) that's between them
    '''
    #simple case
    interim = abs(angle1-angle2)

    #in case angle1 is in 1st quadrant, angle2 is in 4th
    if interim < -360:
        interim = 360 + interim     #add 360 to get the correct angle
    
    #reflex angle case
    if interim > 180:
        interim = 360 - interim     #find the complementary

    return interim

def CosineRule(SideB, SideC, Adeg):
    #returns the length of the side opposite of angle A, if we know sides B and C
    SideA = math.sqrt(SideB*SideB + SideC*SideC - 2*SideB*SideC*math.cos(math.radians(Adeg)))
    #print(SideA)
    return SideA

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

#=============================================

def FindCPA (Bearing1_deg, Range1, Time1, Bearing2_deg, Range2, Time2):
    if Range2 < Range1: 
        #find interim angle (abs)
        InterAngle = FindInterim(Bearing1_deg, Bearing2_deg)
        
        #find interim angle (not abs)
        interim = Bearing2_deg - Bearing1_deg
        if interim < -180:
            while interim < -180:
                interim = interim + 180
        if interim > 180:
            while interim > 180:
                interim = interim - 180
        #TODO check that itnerim gives proper angles, not over 180 or below -180

        #form triangle to get the remaining data on triangle
        Triangle = FindWrongAngle(InterAngle, Range1, Range2)
        #print(Range1, Range2)
        #print(Triangle[0])
        
        #if triangle is proper
        if Triangle[0] != -1:
            #Assign the angles to variables   
            Bearing1_angle = Triangle[2]
            Bearing2_angle = Triangle[1]

            #supplementary angles
            Bearing1_suppl = 180 - Bearing1_angle
            Bearing2_suppl = 180 - Bearing2_angle
        else:
            return -1


        #make the bearings into cartesians
        x1, y1 = bearing_to_cartesian(Bearing1_deg, Range1)
        x2, y2 = bearing_to_cartesian(Bearing2_deg, Range2)
        #print(x1, y1)
        #print(x2, y2)

        #produce movement vector
        dx = x2 - x1
        dy = y2 - y1
        print(dx, dy)

        #distance covered 
        distance_covered = math.sqrt(dx*dx + dy*dy)

        #sine rule to find CPA distance
        CPA_distance = Range2*math.sin(math.radians(Bearing2_suppl))
        
        #pythagorean theorem to find the distance still in need of covering
        distance_to_cover = math.sqrt(Range2**2- CPA_distance**2)
        
        #finding the angle between Bearing 2 and CPA
        InitBearing = 90 - Bearing2_suppl
        
        #direction of CPA
        if interim < 0:
            #counter-clockwise direction

            #finding CPA bearing from bow
            CPA_Bearing = Bearing2_deg - InitBearing
        else:
            #clockwise direction
            CPA_Bearing = Bearing2_deg + InitBearing

        #correcting for negative 
        if CPA_Bearing < 0:
            print("correcting CPA Bearing -")
            while CPA_Bearing < 360:
                CPA_Bearing = 360 + CPA_Bearing
        
        #correcting for over positive
        if CPA_Bearing > 360:
            print("correcting CPA Bearing+")
            while CPA_Bearing > 360:
                CPA_Bearing = CPA_Bearing - 360
        
        #finding the speed
        target_RMS = distance_covered/(Time2-Time1)
        
        #finding the time till CPA happens
        CPA_Eta = distance_to_cover / target_RMS

        #global time value of CPA
        CPA_Time = CPA_Eta + Time2
        
        #=========================
        #printouts
        print("CPA_Bearing = "+ str(CPA_Bearing))
        print("CPA_Distance = "+ str(CPA_distance))
        if CPA_Eta < 0:
            print("CPA is in the past")
            print("CPA_Time = "+ str(CPA_Time))
        else:    
            print("CPA_ETA = "+ str(CPA_Eta))
            print("CPA_Time = "+ str(CPA_Time))
        print("Target RMS = "+ str(target_RMS))
    else:
        print("CPA is in the past")


#print("=======================================================================")


#variable declaration
b1 = 176
r1 = 9.8
t1 = 1206
b2 = 172
r2 = 8.2
t2 = 1212

#arr = FormTriangleAngle(20, 20, 15)
#print(arr)
FindCPA(b1, r1, t1, b2, r2, t2)

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
