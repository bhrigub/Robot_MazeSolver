# Slaughterbot Go scripts and API
"""
@author: Achin, Bhrigu, Frank
References: https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
"""
import sys

sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy

class SlaughterBot():
    def __init__(self):
        self.gpg = easy.EasyGoPiGo3()
	self.distance_sensor = self.gpg.init_distance_sensor()

    #Get a single reading from the distance sensor.
    def read_single_distance(self):
        return self.distance_sensor.read_mm()
    
    

# Turn the distance sensor some number of degrees 
# (specified by an argument) right/left
    def turn_distance_sensor(degrees):
        pass

# Turn wheel 1 or 2 forward or backward independently 
# (this can be several functions, or a single function 
# that takes arguments).
    def wheelmove_time_distance(time_or_distance_parameter, td_value):
        if (time_or_distance_parameter == "time"):          
            self.gpg.forward()
            self.time.sleep(td_value)
        else:
            self.gpg.drive_cm(td_value, True)

    def turn_wheels (movement_direction):
        if (movement_direction) == "forward"):
            self.gpg.forward()
        elif (movement_direction) == "backward"):
            self.gpg.backward()
        elif (movement_direction) == "left"):
            self.gpg.left()
        elif (movement_direction) == "right"):
            self.gpg.right()
        else:
            self.gpg.stop()


#Control the wheels together to turn the robot 90 degrees right/left

#Control the wheels together to t urn some number of degrees (specified by an argument) 
#right/left

#Turn the wheels in order to move the robot a specified distance forward or back (in cm).

#Get a continuous stream of readings from the distance sensor.

#Read the en coders position, in degrees. (See 
#github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py)

#Print the encoders positions in a continuous stream.

def main():
    # do stuff
    pass

if __name__ == "__main__":
    main()
