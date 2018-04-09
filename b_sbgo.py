# Slaughterbot Go scripts and API
"""
@author: Achin, Bhrigu, Frank
References: https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
"""
import sys
import time
sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy

class SlaughterBot():
    def __init__(self):
        self.gpg = easy.EasyGoPiGo3()
        self.DEFAULT_SPEED = 300

	     #self.distance_sensor = self.gpg.init_distance_sensor()
        #self.forward_move=self.gpg.forward()
        #self.backward_move=self.gpg.backward()
        #self.left_move=self.gpg.left()
        #self.right_move=self.gpg.right()
        #self.stop_move=self.gpg.stop()
        #self.drive_cm2=self.gpg.drive_cm()
        
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
#    def wheelmove_time_distance(self,time_or_distance_parameter, td_value):
#        if (time_or_distance_parameter == "time"):          
#            self.forward()
#            time.sleep(td_value)
#        else:
#            self.drive_cm2(td_value, True)

    def turn_wheels (self,movement_direction):
        if (movement_direction == "forward"):
            gpg.forward()
        elif (movement_direction == "backward"):
            gpg.backward()
        elif (movement_direction == "left"):
            gpg.left()
        elif (movement == "right"):
            gpg.right()
        else:
            gpg.stop()


#Control the wheels together to turn the robot 90 degrees right/left

#Control the wheels together to t urn some number of degrees (specified by an argument) 
#right/left

#Turn the wheels in order to move the robot a specified distance forward or back (in cm).

#Get a continuous stream of readings from the distance sensor.

#Read the en coders position, in degrees. (See 
#github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py)

#Print the encoders positions in a continuous stream.

def main():
    gopigo=SlaughterBot()
#    temp = 1
#    gopigo.turn_wheels (temp)
#    time.sleep (1)
#    temp = 2
#    gopigo.turn_wheels (temp)
#    time.sleep (1)
#    temp = 3
#    gopigo.turn_wheels (temp)
#    time.sleep (1)
#    temp = 4
#    gopigo.turn_wheels (temp)
#    time.sleep (1)
#                time.sleep (1)
    for i in range(0,10):
        if i < 5:
            if i % 2 == 1:
                gopigo.turn_wheels ("forward")
                time.sleep (1)
            else:
                gopigo.turn_wheels ("backward")
                time.sleep (1)
        else:
            if i % 2 == 1:
                gopigo.turn_wheels ("left")
                time.sleep (1)
            else:
                gopigo.turn_wheels ("right")
                time.sleep (1)
    pass

if __name__ == "__main__":
    main()
