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
                MA = Matrix[i - (flag/2)][1]
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