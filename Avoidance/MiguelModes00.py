def CameraTestVer00 (detections, AngleThres, DistanceThres):
    ldetec = len(detections)   #assuming detections[type][distance][angle]
    i = 0
    if ldetec > 0:
        while i < ldetec:
            if detections[i][2] < -AngleThres and detections[i][0] == 1:   #Veers left from big buoy
                TurnCommand(R, -detections[i][2], GPSCoordNow())  #corrective command, turns right by as many degrees(?) from current coord
            if detections[i][2] > AngleThres and detections[i][0] == 1:   #veers right from big buoy
                TurnCommand(L, detections[i][2], GPSCoordNow()) #corrective command, turns Left by as many degrees from current coord
            if detections[i][1] < DistanceThres and detections[i][0] == 2: #small buoy is close
                EngageManeuverMode(detections[i])
            if detections[i][1] < DistanceThres and detections[i][0] == 1: #big buoy is close
                EngageTurningMode(detections[i])
            i += 1

def CameraTestVer01 (detections, AngleThres, DistanceThres):
    ldetec = len(detections)   #assuming detections[type][distance][angle]
    i = 0
    flagsmall = 0
    flagbig = 0
    flagsmallid = 0
    flagbigid = 0
    if ldetec > 0:
        while i < ldetec:
            if detections[i][2] < -AngleThres and detections[i][0] == 1:   #Veers left from big buoy
                TurnCommand(R, -detections[i][2], GPSCoordNow())  #corrective command, turns right by as many degrees(?) from current coord
            if detections[i][2] > AngleThres and detections[i][0] == 1:   #veers right from big buoy
                TurnCommand(L, detections[i][2], GPSCoordNow()) #corrective command, turns Left by as many degrees from current coord
            if detections[i][1] < DistanceThres and detections[i][0] == 2: #small buoy is close
                flagsmall += 1          #flags position and number of buoys, used for error checking
                flagsmallid = i         #if there's too many flags, ie >1, we have multiple buoys of the same type ahead, which is uh, problematic
                #EngageManeuverMode(detections[i])
            if detections[i][1] < DistanceThres and detections[i][0] == 1: #big buoy is close
                flagbig += 1
                flagbigid = i
                #EngageTurningMode(detections[i])
            i += 1
        if flagsmall > 0:
            if flagsmall > 1:
                print("???")
            EngageManeuverMode(detections[flagsmallid])
        if flagbig > 0:
            if flagbig >1:
                print("???")
            EngageTurningMode(detections[flagbigid])

def CameraTestVer02 (detections, AngleThres, DistanceThres):
    ldetec = len(detections)   #assuming detections[type][distance][angle]
    i = 0
    flagsmall = 0
    flagbig = 0
    flagsmallid = 0
    flagbigid = 0
    if ldetec > 0:
        while i < ldetec:
            if detections[i][2] < -AngleThres and detections[i][0] == 1:   #Veers left from big buoy
                TurnCommand(R, -detections[i][2], GPSCoordNow())  #corrective command, turns right by as many degrees(?) from current coord
            if detections[i][2] > AngleThres and detections[i][0] == 1:   #veers right from big buoy
                TurnCommand(L, detections[i][2], GPSCoordNow()) #corrective command, turns Left by as many degrees from current coord
            if detections[i][1] < DistanceThres and detections[i][0] == 2: #small buoy is close
                flagsmall += 1          #flags position and number of buoys, used for error checking
                flagsmallid = i         #if there's too many flags, ie >1, we have multiple buoys of the same type ahead, which is uh, problematic
                #EngageManeuverMode(detections[i])
            if detections[i][1] < DistanceThres and detections[i][0] == 1: #big buoy is close
                flagbig += 1
                flagbigid = i
                #EngageTurningMode(detections[i])
            i += 1
        if flagsmall > 0:
            if flagsmall == 1:
                EngageManeuverMode(detections[flagsmallid])
            else:
                print("multiple small buoys in camera")
                idkwhatdo()
            #can probably remove flagsmall == 1 and the "else" as a safety issue. if there's a small buoy detected within range, just move to maneuver mode to be safe. 
            #TODO CALIBRATION OF THIS
        #if flagsmall > 0:
        #   EngageManeuverMode(detections[flagsmallid])
        if flagbig > 0:
            if flagbig == 1:
                EngageTurningMode(detections[flagbigid])
            else:
                print("multiple large buoys in camera")
                idkwhatdo()
        #ssame concern as above. can be simplified


def TurnCommand(Direction, Angle, currect coordinates):
    print ("hi")

def GPSCoordNow():
    print ("hii")
    return "gps coord"

def EngageManeuverMode(obstacle):
    print("hiii")

def EngageTurningMode(buoy, anglethres, distthres):
    #buoy is [2][distance][angle]
    #buoy must be acknowledge by lidar first before movement is done
    #anglethres = the half of the range for which we consider the detected object to be the same
    #distthres same as above but for strength
    #big buoy = 1400mm in length. I assume that its a bit smaller on average due to our sensor's increased height. 
    #600-1500 is the acceptable (?) lengths for it. 
    #TODO HECCING TEST THIS.
    #I DONT CARE, TAKE THE BOAT OUT, TAKE THE BUOY OUT AND FRICKING MEASURE ALL THE VARIANCE WE CAN GET
    #I'M MAKING A PURELY HYPOTHETICAL PROGRAMME THAT I DONT EVEN KNOW IF IT WORKS, I CANT DEBUG IF I CANT RUN IT TO TEST IT
    i = 0
    while i < 10:
        lidardet = []
        lidardet = CompareScans(ProcessScan(get_scan(), 0.5, 3, 12), ProcessScan(get_scan(), 0.5, 3, 12), 12, 5, 120, 150)
        if len(lidardet) > 0:
            j = 0
            while j < len(lidardet):
                if lidardet[j][2] > buoyanglemin and lidardet[j][2] < buoyanglemax:
                    if lidardet[j][3] > buoydistancemin and lidardet[j][3] < buoydistancemax:



    print("hiiii")

def idkwhatdo():
    print("\(-.-)/")
    print("idk what to do here")
    print("Praise the Omnissiah. Only He knows what's wrong with this programme")







