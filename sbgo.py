# Slaughterbot Go scripts and API
<<<<<<< HEAD
# Authors: A, B, F
# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
import multiprocessing as mp

import sys
import time
=======
"""
@author: Achin, Bhrigu, Frank
References: https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
"""
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division 
>>>>>>> bBranch

import sys
import time
sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy
 

class SlaughterBot():
    def __init__(self, distance_hz=0):
        self.gpg = easy.EasyGoPiGo3()
<<<<<<< HEAD
	self.distance_sensor = self.gpg.init_distance_sensor()
	self.distance_hz = distance_hz
        self.current_distance = mp.Value('i', 0)

    # Get a single cm reading from the distance sensor.
    # Attribution: code used from GoPiGo3 software found at:
    # https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
    def read_single_distance(self):
        return self.distance_sensor.read()

    # Attribution: code used from GoPiGo3 software found at:
    # https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
    def read_continuous_distance(self):
        if self.distance_hz <= 0:
            delay = 0
        else:
            delay = 1.0/self.distance_hz
	try:
            while True:
		self.current_distance = self.read_single_distance()
		print("Current distance: {}".format(self.current_distance))
                time.sleep(delay)
        except KeyboardInterrupt:
            self.gpg.reset_all()

def main():
    bot = SlaughterBot(4)
    # let's start the continuous distance readings in another thread
    p = mp.Process(target=bot.read_continuous_distance)
    p.start()

    # Simple algorithm to demonstrate proof of life
    # Move forward until distance is 10cm or less
    while bot.current_distance > 10:
	bot.move_forward()

    # Turn to the right 90 degrees
    bot.turn_right(90)

    # Aim distance sensor servo at wall
    bot.turn_servo(180)

    while bot.current_distance > 10:
        bot.move_forward() 
=======
        self.DEFAULT_SPEED = 300
        
    #Get a single reading from the distance sensor.
    def read_single_distance(self):
        return self.distance_sensor.read_mm()
    


#Function Objective: Move robot- Forward, Backward, Left, Right
#Input Strings: forward, backward, left, right
#Default Action: Stop

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
            time.sleep(2)

			

#Function Objective: Move robot 'X' cm distance 
#Input Strings: Distance value in cm
#Default Action: N/A

    def move_distance (self,distance_val):
        self.gpg.drive_cm(distance_val,True)


#Function Objective: Turn robot by 'X' degree using both the wheels 
#Input Strings: Rotation value in degree
#Default Action: N/A

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
        

#Function Objective: Turn individual robot wheel 
#Input Strings: Wheel selection string - leftf, leftb, rightf, rightb
#Default Action: Stop

    def turn_wheel(self, wheel_turn):
        if (wheel_turn== "leftf"):
            self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT, 0)
            self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT, self.gpg.get_speed())
        elif (wheel_turn== "leftb"):
            self.gpg.set_motor_dps(-self.gpg.MOTOR_LEFT, -self.gpg.get_speed())
            self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT, 0)
        elif (wheel_turn== "rightf"):
            self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT, 0)
            self.gpg.set_motor_dps(self.gpg.MOTOR_RIGHT, self.gpg.get_speed())
        elif (wheel_turn== "rightb"):
            self.gpg.set_motor_dps(self.gpg.MOTOR_LEFT, 0)
            self.gpg.set_motor_dps(-self.gpg.MOTOR_RIGHT, -self.gpg.get_speed())
        else:
            self.turn_degrees(0,0)
            time.sleep(2)


def main():
    gopigo=SlaughterBot()

    
    gopigo.move_robot ("forward")
    time.sleep (3)
    gopigo.move_robot ("left")
    time.sleep (3)
    gopigo.move_robot ("right")
    time.sleep (3)
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
  

    gopigo.move_distance(10)
    

>>>>>>> bBranch

if __name__ == "__main__":
    main()
