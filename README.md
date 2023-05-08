lidar github
general overview

Raw lidar data -> translation -> scan identification -> object detection -> danger estimation -> maneuver creation

raw lidar data: QUALITY (0-15)[customary units], Angle (XXX.XXXXXX [yes, six decimals.])[in deg], Distance (YYYY.YY) [in mm]

translation: pairnoume raw lidar data kai vgazoume array apo *1* rotation gia na perasei sto ID phase. (Fail cond: angles, and shiet)

scan id: find what might be considered "objects" from 1 scan. returns list of possible objects. (pass more stuff, starting/ending angle, avg dist & shit)

object det: takes two/three lists of objects and find how many of those are "close" enough for them to be considered the same

danger estimation: who is a danger to my vessel. anything front/heading towards me

maneuver creation: given the vessel's current GPS cood, generate a GPS coordinate path to avoid said danger
