


def CompareScans(Scan1, Scan2):
    StartingAngleThres = 0.5
    EndingAngleThres = 0.5
    MeanAngleThres = 0.5
    MeanDistThres = 0.5
    #LengthThres = 0.5
    flagSA = 0
    flagEA = 0
    flagMA = 0
    flagMD = 0
    i = 0
    while i < len(Scan1):
        Sad = abs(Scan1[i][][] - Scan2[i][][]) #StartingAngleDifference
        Ead = abs(Scan1[i][][] - Scan2[i][][]) #EndingAngleDifference
        Mad = abs(Scan1[i][][] - Scan2[i][][]) #MeanAngleDifference
        Mdd = abs(Scan1[i][][] - Scan2[i][][]) #MeanDistanceDifference
        #LengthDist
    #--------------------------------------
        if Sad < StartingAngleThres :
            flagSA = 1
        else:
            flagSA = 0
    #--------------------------------------
        if Ead < EndingAngleThres :
            flagEA = 1
        else:
            flagEA = 0
    #--------------------------------------
        if Mad < MeanAngleThres :
            flagMA = 1
        else:
            flagMA = 0
    #--------------------------------------
        if Mdd < MeanDistThres :
            flagMD = 1
        else:
            flagMD = 0
    #--------------------------------------
    if (flagSA*2 + flagEA*2












