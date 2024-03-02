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
            if abs(Scan1[i][3] - Scan2[j][3]) < DistThres:
                flagL = True
            j +=1
            if FlagQ and FlagA and FlagD and FlagL: #not sure if it must be AND for all. could do OR or XOR or smth               
                templ = []
                templ.append(Scan1[i])
                templ.append(Scan2[j])
                Objectslist.append(templ)
                templ = []
                print(scan2[j][1], scan2[j][2], ' ', scan1[i][1], scan1[i][2])
                break
        i += 1
    return Objectslist