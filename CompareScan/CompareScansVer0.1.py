def compare_scans(scan1, scan2, anglethres, distthres):
    #print('entry to compare scans')
    i = 0
    j = 0
    Objectslist = []
    #print(here)
    while i < len(scan1):
        flag1 = 0
        flag2 = 0
        #print(here)
        while j < len(scan2):
            if abs(scan1[i][1] - scan2[j][1]) < anglethres:
                flag1 = 1
                #print(here)
                break
            if abs(scan1[i][2] - scan2[j][2]) < distthres:
                flag2 = 1
                #print(here)
                break
            j +=1
        if flag1 == 1 and flag2 == 1:
            templ = []
            templ = (scan2[j][0], scan2[j][1], scan2[j][2])
            Objectslist.append(templ)
            print(scan2[j][1], scan2[j][2], ' ', scan1[i][1], scan1[i][2])
            #print(here)
            break
        i += 1
    #print('exit from compare scans')
    return Objectslist