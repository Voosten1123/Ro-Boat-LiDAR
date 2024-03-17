import math

pi = 3.14159265358979323846


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