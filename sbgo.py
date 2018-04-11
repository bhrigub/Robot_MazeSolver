# Slaughterbot Go scripts and API
# Authors: A, B, F
# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division 


import multiprocessing as mp
import sys
import time

sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy
 

class SlaughterBot():
    def __init__(self, distance_hz=0):
        self.gpg = easy.EasyGoPiGo3()
        self.distance_sensor = self.gpg.init_distance_sensor()
	self.servo = self.gpg.init_servo("SERVO2")
        self.distance_hz = distance_hz
        self.current_distance = mp.Value('i', 0)

 

#Turn the distance sensor some number of degrees (specified by an argument) right/left
    def turn_distance_sensor(self, degrees):
        self.servo.rotate_servo(degrees)
     

# Turn left/right wheel forward and both wheels simultaneously forward or backward.
    def turn_wheels(self, direction):
            if direction == 1:
                try:
                    self.gpg.left()
                except KeyboardInterrupt:
                    self.gpg.reset_all()
            if direction == 2:
                try:
                    self.gpg.right()
                except KeyboardInterrupt:
                    self.gpg.reset_all()
            if direction == 3:
                try:
                    self.gpg.forward()
                except KeyboardInterrupt:
                    self.gpg.reset_all()
            if direction == 4:
                try:
                    self.gpg.backward()
                except KeyboardInterrupt:
                    self.gpg.reset_all()
            if direction == 5:
                    self.gpg.stop() 


#Control the wheels together to turn the robot 90 degrees right/left
#Control the wheels together to turn the robot 90 degrees right/left
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


#Control the wheels together to turn some number of degrees (specified by an argument)
#right/left


    #Turn the wheels in order to move the robot a specified distance forward or back (in cm).
    def drive_dist(self, distance):
        self.gpg.drive_cm(distance)


    #Get a single reading from the distance sensor.
    def read_single_distance(self):
        return self.distance_sensor.read()


    #Get a continuous stream of readings from the distance sensor.
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


    #Read the encoders position in degrees. 
    #Print the encoders positions in a continuous stream.
    def read_encoders(self):
        try:
            while True:
                print("Encoders positions (degrees): " + str(self.gpg.read_encoders()))
        except KeyboardInterrupt:
            self.gpg.reset_all()
            self.gpg.reset_encoders() 
    

def main():
    #create class object(s)
    bot = SlaughterBot(4)

    ##9a. turn_distance_sensor some number of degrees (left -> 0-89 degrees right -> 91-180 degrees) 
    #degrees = input("Enter degrees to rotate:: ")
    #bot.turn_distance_sensor(degrees)

  
    ##9b. turn wheel 1 or 2 forward or backward independently
    #Forward left
    #bot.turn_wheel ("leftf")
    #Backward left
    #bot.turn_wheel ("leftb")
    #Forward right
    #bot.turn_wheel ("rightf")
    #Backward right
    #bot.turn_wheel ("rightb")


    ##9c. Control the wheels to move the robot forward or backward
    #bot.move_robot ("forward")
    #bot.move_robot ("backward")
    

    ##9d. Control the wheels together to turn the robot 90 degrees right/left
    #bot.move_robot ("left")
    #bot.move_robot ("right")
  
    
    ##9e. Control the wheels together to turn the robot some number of degrees right/left
    #bot.turn_degrees(30,180)
    #bot.turn_degrees(45,180)


    ##9f. Turn wheels to move the robot a specified distance forward or backward(in cm)
    # (10) forward and (-10) for backward
    #bot.move_distance(10)


    ##10a, 10b Distance sensor readings
    #bot.read_single_distance()
    #bot.read_continuous_distance()


    ##10c. read encoders position in degrees and print readings in continuous stream
    #bot.read_encoders()


    #robot incorporated
    #p = mp.Process(target=bot.read_continuous_distance)
    #p.start()
   
    while bot.read_single_distance() > 10:
	     bot.turn_wheels(3)
    bot.turn_wheels(5)
    bot.move_robot("right")
    time.sleep(1)
    bot.turn_distance_sensor(180)
    time.sleep(1)
    while bot.read_single_distance() >= 10:
        bot.move_distance(40)
        time.sleep(1)
        break


if __name__ == "__main__":
    main()

