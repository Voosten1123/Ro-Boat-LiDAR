
from pickle import NONE, TRUE

#////////////////CLASSES////////////////////
class measurement:
    def __init__(self, angle, distance, strength):
        self.angle = angle
        self.distance = distance
        self.strength = strength
    def check_return(self):
        if self.strength > 0:
            return TRUE

class sierra: #objects identified by Lidar
    def __init__(self, distance): #for now each object is only identified by the distance from its closest point 
        self.distance = distance
        self.associated_points = []
    
#////////////////END_OF_CLASSES////////////////////

#////////////////FUNCTIONS////////////////////
def association(current_dis, next_dis): #probably needs a check return thing too
    Minimum_acceptable_distance = 5 #minimum distance between two points for them to be considered cohesive
    if abs(current_dis - next_dis) < Minimum_acceptable_distance:
        return TRUE

def closest_point(clos, pre, crnt): #compares current closests point of a single object with two contenders (previous point and current point)
        if clos == None or clos < pre:
            clos = pre # set the first point spotted as the closests, will check if nxt is closer later in the association
        elif clos < crnt:
            clos = crnt

#////////////////END_OF_FUNCTIONS////////////////////
#measurements are defined as objects with // flaot:angle (0-360) // float:distance (0-11850) // int:strength (0-2000) // bool:new_scan (ignoring new_scan for now)
#for now we assume that all measurements are in a list called theList
theList = []

ListOfSierra = [] #objects identified by Lidar get stored here contains 

templi = [] #temp to store all associated measurements of an object

i = 1 #start from 1 so that it doesnt cause an error on the first iteration

as_flag = False #flag used to mark the start and end of an association

for measurement in theList:
    if measurement.check_return :
        pre_measurement = theList[theList.index(measurement.distance)-1]
        if association(measurement.distance, pre_measurement): #associates current measurement with previous measurement looking for cohesion
            clos = closest_point(clos, pre_measurement, measurement.distance)
            templi.append(pre_measurement)
            as_flag = True
        elif as_flag:
            templi.append(pre_measurement) #gets last associated point, note that its distance is not taking into account for closest_point hence there is an error margin of Minimum_acceptable_distance
            ListOfSierra.append(sierra(clos).associated_points.append(templi)) #appends full object into List Of Sierra
            as_flag = False #resets association flag
            templi.clear() #resets associated points
    elif as_flag:
        templi.append(pre_measurement) #gets last associated point, note that its distance is not taking into account for closest_point hence there is an error margin of Minimum_acceptable_distance
        ListOfSierra.append(sierra(clos).associated_points.append(templi)) #appends full object into List Of Sierra
        as_flag = False #resets association flag
        templi.clear() #resets associated points
        #I should do these 4 lines a function probably 

            

        


        
