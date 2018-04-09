# Slaughterbot Go scripts and API
"""
@author: Achin, Bhrigu, Frank
References: https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
"""
import sys
import time
sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division  

class SlaughterBot():
    def __init__(self):
        self.gpg = easy.EasyGoPiGo3()
        self.DEFAULT_SPEED = 300
        
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
#        if (movement_direction == "forward"):
#            self.gpg.forward()
#        elif (movement_direction == "backward"):
#            self.gpg.backward()
#        elif (movement_direction == "left"):
#            self.gpg.left()
#        elif (movement_direction == "right"):
#            self.gpg.right()
#        else:
#            self.gpg.stop()
        if (movement_direction == "forward"):
            self.gpg.forward()
        elif (movement_direction == "backward"):
            self.gpg.backward()
        elif (movement_direction == "left"):
            self.turnDegrees(-90,100)
        elif (movement_direction == "right"):
            self.turnDegrees(90,100)
        else:
            self.turnDegrees(0,0)

    def turnDegrees(self, degrees, speed):
        # get the starting position of each motor
        StartPositionLeft      = self.gpg.get_motor_encoder(self.gpg.MOTOR_LEFT)
        StartPositionRight     = self.gpg.get_motor_encoder(self.gpg.MOTOR_RIGHT)
        
        # the distance in mm that each wheel needs to travel
        WheelTravelDistance    = ((self.gpg.WHEEL_BASE_CIRCUMFERENCE * degrees) / 360)
        
        # the number of degrees each wheel needs to turn
        WheelTurnDegrees       = ((WheelTravelDistance / self.gpg.WHEEL_CIRCUMFERENCE) * 360)
        
        # Limit the speed
        self.gpg.set_motor_limits(self.gpg.MOTOR_LEFT + self.gpg.MOTOR_RIGHT, dps = speed)
        
        # Set each motor target
        self.gpg.set_motor_position(self.gpg.MOTOR_LEFT, (StartPositionLeft + WheelTurnDegrees))
        self.gpg.set_motor_position(self.gpg.MOTOR_RIGHT, (StartPositionRight - WheelTurnDegrees))
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

    for i in range(0,12):
        if i < 5:
            if i % 2 == 1:
                gopigo.turn_wheels ("forward")
                time.sleep (1)
            else:
                gopigo.turn_wheels ("backward")
                time.sleep (1)
        elif i<10:
            if i % 2 == 1:
                gopigo.turn_wheels ("left")
                time.sleep (1)
            else:
                gopigo.turn_wheels ("right")
                time.sleep (1)
        else:
            gopigo.turn_wheels ("boomchikiboom")
    pass

if __name__ == "__main__":
    main()
