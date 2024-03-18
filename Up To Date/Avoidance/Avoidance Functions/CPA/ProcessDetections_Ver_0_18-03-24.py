import math

#for plotting
import matplotlib.pyplot as plt 
import matplotlib.transforms as mtransforms 
#import numpy as np 
from matplotlib.transforms import offset_copy 

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
    Brad = math.asin((SideB*sin(Adeg))/SideA)
    Crad = math.asin((SideC*sin(Adeg))/SideA)

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
            #print("====\nchanged B\n====")
            return 1, Bdeg, Cdeg
        elif round(ABCC) == 180:    #if C is wrong
            Cdeg = Cdeg_alt         #change C to the alternative
            #print("====\nchanged C\n====")
            return 2, Bdeg, Cdeg
        else:
            print("failed to make a triangle")      #safety
            #print("Angle A : " + str(Adeg)+ " || Angle B : " + str(Bdeg)+ " || Angle C : " + str(Cdeg)) #for checking
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

def sin(deg):
    sine = math.sin(math.radians(deg))
    return sine

def cosine(deg):
    cosine = math.cos(math.radians(deg))
    return cosine

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

def Vector_length(X, Y):
    #mathematical vector length
    l = math.sqrt(X**2 + Y**2)
    return l

def correct_angle(angle):
    #takes an angle in degrees, checks to see if its within the circle, otherwise, adds/removes until it is
    
    if angle > 360:
        
        while angle > 360:
            
            angle = angle - 360
    
    if angle < 0:
        
        while angle < 0:
            
            angle = angle + 360
    
    return angle

def Process_Det(Spd, Brg1, Rng1, T1, Brg2, Rng2, T2):

    #getting cartesian coords
    x1, y1 = bearing_to_cartesian(Brg1, Rng1)
    x2, y2 = bearing_to_cartesian(Brg2, Rng2)

    #finding vectors
    dx = x2 - x1
    dy = y2 - y1

    #time difference (should always be positive)    
    time_diff = T2 - T1
    if time_diff < 0:
        print("time error || time difference negative")
        return -1

    #angle between bearings
    inter = Brg2 - Brg1
    if inter < -180:
        while inter < -180:
            inter = inter + 180
    if inter > 180:
        while inter > 180:
            inter = inter - 180

    #distance covered by target inbetween detections
    dist_cov = math.sqrt(Rng1**2 + Rng2**2 - 2 * Rng1 * Rng2 * cosine(inter) )

    #in the Triangle: (US[A] - Detection2[B] - Detection1[C]), finding the interion angle for detection 2
    #B2_angle = math.asin( (Rng1*sin(inter)) / dist_cov)
    #B2_angle = math.degrees(B2_angle)       #TODO fix wrong angle here

    #finding both remaining angles
    Triangle = FindWrongAngle(inter, Rng1, Rng2)
    
    #if triangle is proper
    if Triangle[0] != -1:
        #Assign the angles to variables   
        B2_angle = Triangle[1]
        #B1_angle = Triangle[2]     #unneeded atm
        
        #supplementary angles
        B2_suppl = 180 - B2_angle
        #B1_suppl = 180 - B1_angle      #unneeded atm
    else:
        print("Bearing Error || cannot form triangle")
        return -1

    #CPA Distance. Through sine rule
    CPA_d = abs(sin(B2_suppl)) * Rng2

    #angle between CPA Bearing and Bearing 2
    brg_diff = 90 - abs(B2_suppl)

    #Distance To Cover. Through sine rule again
    dist2c = sin(brg_diff) * Rng2

    #Relatime Motion Speed
    rms = dist_cov / time_diff

    #CPA Time
    CPA_t = dist2c / rms

    #Distance that our vessel has covered between the two detections
    our_dist = Spd * time_diff

    #checking if vessel is coming clockwise or anti clockwise
    #so we can then add/subtract the angle between CPA and Brg2
    if inter == 0:
        CPA_b = 0
    elif inter < 0:
        CPA_b = Brg2 - brg_diff  
    else:
        CPA_b = Brg2 + brg_diff

    #correcting for <0 and >360
    CPA_b = correct_angle(CPA_b)
    
    #True Course. tan (TCRS) = dx [opposite] / our_dist [adjacent]
    TCRS = math.atan(dx / our_dist)
    TCRS = math.degrees(TCRS)
    TCRS = correct_angle(TCRS)

    #true distance covered. hypoteneuse
    tdst = math.sqrt( dx**2 + our_dist**2)

    #True Speed
    TSPD = tdst / time_diff

    #printouts
    print("\nFor:")
    print("Vessel Speed : " + str(Spd) + " m/s, and Course : " + str(dy))
    print("Brg 1: "+ str(Brg1) + " | 2: " + str(Brg2) + " Degrees off Bow")
    print("Rng 1: "+ str(Rng1) + " | 2: " + str(Rng2) + " Meters from the ship")
    print("Time 1: "+ str(T1) + " | 2: " + str(T2) + " seconds")
    print("==========================")
    print("CPA Brg : " + str(CPA_b))
    print("CPA Time : " + str(CPA_t))
    print("CPA Dist : " + str(CPA_d))
    print("TCRS : " + str(TCRS))
    print("TSPD : " + str(TSPD))
    print("==========================\n")


crs = 0
t1 = 1301
b1 = 320
r1 = 3600
t2 = 1313
b2 = 292
r2 = 1200
spd = 50


print("========")
Process_Det(spd, b1, r1, t1, b2, r2, t2)

print("========")
#Process_Det(spd, b2, r2, t2, b3, r3, t3)


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
#plt.show()