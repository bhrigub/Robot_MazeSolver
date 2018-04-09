# Slaughterbot Go scripts and API
"""
@author: Achin, Bhrigu, Frank
References: https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
"""
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division 

import sys
import time
sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy
 

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

    def move_robot (self,movement_direction):
        if (movement_direction == "forward"):
            self.gpg.forward()
        elif (movement_direction == "backward"):
            self.gpg.backward()
        elif (movement_direction == "left"):
            self.turn_degrees(-90,180)
        elif (movement_direction == "right"):
            self.turn_degrees(90,180)
        else:
            self.turn_degrees(0,0)

    def turn_degrees(self, degrees, speed):
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
        
    def turn_wheel(self, wheel_turn):
        if (wheel_turn== "leftf"):
            #self.gpg.left()
            self.gpg.set_motor_position(self.gpg.MOTOR_LEFT, 150)
            #self.gpg.set_motor_position(self.gpg.MOTOR_RIGHT, 0)
        elif (wheel_turn== "leftb"):
            #self.gpg.right()
            self.gpg.set_motor_position(self.gpg.MOTOR_LEFT, -150)
            #self.gpg.set_motor_position(self.gpg.MOTOR_RIGHT, 0)
        elif (wheel_turn== "rightf"):
            #self.gpg.right()
            #self.gpg.set_motor_position(self.gpg.MOTOR_LEFT, 0)
            self.gpg.set_motor_position(self.gpg.MOTOR_RIGHT, 150)
        elif (wheel_turn== "rightb"):
            #self.gpg.right()
            #self.gpg.set_motor_position(self.gpg.MOTOR_LEFT, 0)
            self.gpg.set_motor_position(self.gpg.MOTOR_RIGHT, -150)
        else:
            self.turn_degrees(0,0)


def main():
    gopigo=SlaughterBot()
    gopigo.move_robot ("forward")
    time.sleep (1)
    gopigo.move_robot ("left")
    time.sleep (1)
    gopigo.move_robot ("right")
    time.sleep (2)
    gopigo.move_robot ("boomchikiboom")
    gopigo.turn_wheel ("leftf")
    time.sleep (2)
    gopigo.turn_wheel ("leftb")
    time.sleep (2)
    gopigo.turn_wheel ("rightf")
    time.sleep (2)
    gopigo.turn_wheel ("rightb")
    time.sleep (2)
    gopigo.move_robot ("boomchikiboom")
    

#    for i in range(0,12):
#        if i < 5:
#            if i % 2 == 1:
#                gopigo.turn_wheels ("forward")
#                time.sleep (1)
#            else:
#                gopigo.turn_wheels ("backward")
#                time.sleep (1)
#        elif i<10:
#            if i % 2 == 1:
#                gopigo.turn_wheels ("left")
#                time.sleep (1)
#            else:
#                gopigo.turn_wheels ("right")
#                time.sleep (1)
#        else:
#            gopigo.turn_wheels ("boomchikiboom")
#    pass

if __name__ == "__main__":
    main()
