class Target:
    def __init__(self, ID, FromSensor, Bearing, Range, Time, Size, RML, RMS, Mx, NRML, ARML, CPA, CPAtime, CPAbrg, CPAdist, TrueHeading, TrueSpeed)
        self.ID = ID                        #Identification string? integer? of the target
        self.FromSensor = FromSensor        #string indicating which sensor detected the target. if multiple, they're all included (AIS-LIDAR-RADAR-CAMERA, etc)
        self.Bearing = Bearing              #degrees off bow (Bow of ship always points to 000/True North)  [deg]
        self.Range = Range                  #distance to target (in meters) [m]
        self.Time = Time                    #timestamp of the parameters [s]
        self.Size = Size                    #Size of target. [m * m]
        self.RML = RML                      #line showing relative motion between our ship and target 
        self.RMS = RMS                      #relative speed between our ship and target [m/s] (negative = we're moving away from each other, positive = we're approaching each other)
        self.MX = Mx                        #Point of maneuver execution [lat/long] TODO find out about this                TODO discard?
        self.NRML = NRML                    #New RML. Originates from Mx, and is the RML that does NOT intersect our BNG    TODO discard? 
        self.ARML = ARML                    #Advanced RML. originates from last detection, opposite direction of NRML.      TODO discard?
        self.CPA = CPA                      #coordiantes of the CPA (Closest Point of Approach) [lat, long]
        self.CPAtime = CPAtime              #time till CPA is reached [s] (note: NOT the global time of CPA. this is the time UNTIL CPA)
        self.CPAbrg = CPAbrg                #Angle at which CPA will be, relative to bow [deg]
        self.CPAdist = CPAdist              #Distance between CPA and our ship [m]
        self.TrueHeading = TrueHeading      #Target's course [deg]
        self.TrueSpeed = TrueSpeed          #Target's true speed [m/s]


