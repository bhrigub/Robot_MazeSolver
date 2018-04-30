# Slaughterbot Go scripts and API
# Authors: A, B, F
# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/gopigo3.py

from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division 


import multiprocessing as mp
import sys
import time
import math
import random

sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy
 

class SlaughterBot():
    def __init__(self, distance_hz=0):
        self.gpg = easy.EasyGoPiGo3()
        self.distance_sensor = self.gpg.init_distance_sensor()
        self.servo = self.gpg.init_servo("SERVO2")
        self.distance_hz = distance_hz
        self.current_distance = mp.Value('i', 0)

 
# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
#Turn the distance sensor some number of degrees (specified by an argument) right/left
    def turn_distance_sensor(self, degrees):
        self.servo.rotate_servo(degrees)
        time.sleep(1)
     

# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
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


# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
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

			

# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
#Function Objective: Move robot 'X' cm distance 
#Input Strings: Distance value in cm
#Default Action: N/A

    def move_distance (self,distance_val):
        # magic number 20 distance measure for boundary - put in parameters
        if self.current_distance.value > 7:
            self.turn_distance_sensor(90)
            if distance_val>10:
                while distance_val > 0:
                    travel = 5
                    self.move_distance(travel)
		    distance_val = distance_val - 5
		    print("Distance travelled = ", travel)
                    print("Distance trailing = ", distance_val)
            else:
                self.gpg.drive_cm(distance_val, False)
            time.sleep(2)


# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
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
        time.sleep(2)
        

# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
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


# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
#Control the wheels together to turn some number of degrees (specified by an argument)
#right/left


    #Turn the wheels in order to move the robot a specified distance forward or back (in cm).
    def drive_dist(self, distance):
        self.gpg.drive_cm(distance, False)
        time.sleep(2)


# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
    #Get a single reading from the distance sensor.
    def read_single_distance(self):
        return self.distance_sensor.read()


# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
    #Get a continuous stream of readings from the distance sensor.
    def read_continuous_distance(self):
        if self.distance_hz <= 0:
            delay = 0
        else:
            delay = 1.0/self.distance_hz
        try:
            while True:
                self.current_distance.value = self.read_single_distance()
                #print("Current distance: {}".format(self.current_distance.value))
                time.sleep(delay)
        except KeyboardInterrupt:
            self.gpg.reset_all()    


# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
    #Read the encoders position in degrees. 
    #Print the encoders positions in a continuous stream.
    def read_encoders(self):
        try:
            while True:
                print("Encoders positions (degrees): " + str(self.gpg.read_encoders()))
        except KeyboardInterrupt:
            self.gpg.reset_all()
            self.gpg.reset_encoders() 


# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/gopigo3.py
    def read_encoders_avg(self, units):
        WHEEL_CIRCUMFERENCE = 66.5 * math.pi
        left, right = self.gpg.read_encoders()
        average = (left+right)/2
        if units=="cm":
            average = ((average / 360 ) * WHEEL_CIRCUMFERENCE) / 10
            print("Encoders position (cm): " + str(average))
        else:
            pass
            # do no conversion
        return average
    

# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
    def reset_encoders(self):
        self.gpg.reset_encoders()

    # Scans at 45 degree increments for the distances greater than len and
    # returns a list of angles that satisfy
    def scan_distance_angles(self, min_distance, delta_angle):
        i = 0
        angles = []
        self.turn_distance_sensor(90)

        while i <= 180:
            self.turn_distance_sensor(i)
            # magic number 3 for number of sensor readings to average
            distance = self.get_average_distance(3)
            print("distance: {}".format(distance))

            if distance > min_distance:
                angles.append(i)

            i += delta_angle
        self.turn_distance_sensor(90)
        return angles

    # Returns the average distance over len readings
    def get_average_distance(self, len):
        time.sleep(0.25)
        i = 0
        sum = 0
        while i < len:
            sum += self.read_single_distance()
            i += 1

        return sum/len
		

    #Adjusts the robot position before steering towards the corridor
    def holeSubroutine(self, angle):
        holeLength = 0
        while self.current_distance.value >= 15:
            self.gpg.drive_cm(5)
            time.sleep(1)
            holeLength += 5
            self.turn_distance_sensor(90)
            time.sleep(1)
            #print("Turning Distance Sensor 90")
            if self.current_distance.value <10:
                #print("Distance less than 10")
                continue
            else:
                self.turn_distance_sensor(angle)
                time.sleep(1)
                #print("revert")
        self.turn_distance_sensor(angle)
        time.sleep(1)
        print("holeLength= ",holeLength)
        holeLength = (holeLength/2) - 4
        print("Distance reversed= ",holeLength)
        print("current distance= ",self.current_distance.value)
        self.gpg.drive_cm(-holeLength)

    def check_Crash(self): 
	#self.turn_distance_sensor(90)
        self.turn_distance_sensor(0)
        time.sleep(0.25)
        
	dist1= self.get_average_distance(3)
        time.sleep(0.25)
	self.turn_distance_sensor(45)
        time.sleep(0.25)
	dist2= self.get_average_distance(3)
        time.sleep(0.25)
	self.turn_distance_sensor(90)
        time.sleep(0.25)
	dist3= self.get_average_distance(3)
        time.sleep(0.25)
	self.turn_distance_sensor(135)
        time.sleep(0.25)      
	dist4= self.get_average_distance(3)
        time.sleep(0.25)
        self.turn_distance_sensor(180)
        time.sleep(0.25)      
	dist5= self.get_average_distance(3)

	if dist1<10 or dist2<10 or dist3<10 or dist4 <10 or dist5 <10:
	    return 1
	else:
	    return 0

	
    #Calibrate robot
 
    def calibrateJunction2 (self):
	#self.turn_distance_sensor(90)
        self.turn_distance_sensor(0)
        time.sleep(0.25)
        distLeft= self.get_average_distance(3)
        time.sleep(0.25)
        self.turn_distance_sensor(180)
        time.sleep(0.25)
	distRight= self.get_average_distance(3)

        baseLen = 25
        if distRight > 10 and distLeft > 10:
            blah=0

        elif distRight < 20 and distLeft < 20:
            if distRight > distLeft:
                perpendicularLen = (distRight - distLeft) / 2
                angleDisplacement = round(math.degrees(math.atan(perpendicularLen / baseLen)),0)
            elif distRight < distLeft:
                perpendicularLen = (distLeft - distRight) / 2
                angleDisplacement = round(math.degrees(math.atan(perpendicularLen / baseLen)),0)
            self.turn_degrees(angleDisplacement,300)
	    time.sleep(0.25)

            for i in range (0,180,20):
                self.turn_distance_sensor(i)
	        time.sleep(0.25)     
		if self.current_distance.value < 10:
                    self.calibrateJunction()

        elif distRight < 20 and distLeft >20:
            self.turn_degrees(-12,300)
	    time.sleep(0.25)

            for i in range (0,180,20):
                self.turn_distance_sensor(i)
	        time.sleep(0.25)        
		if self.current_distance.value < 10:
                    self.calibrateJunction()
        elif distRight > 20 and distLeft <20:
            self.turn_degrees(12,300)
	    time.sleep(0.25)

            for i in range (0,180,90):
                self.turn_distance_sensor(i)
	        time.sleep(0.25)
 
                if self.current_distance.value < 10:
                    self.calibrateJunction()



    def calibrateJunction (self):
	
	self.turn_distance_sensor(90)
        self.turn_distance_sensor(0)
        distRight= self.get_average_distance(3)
        self.turn_distance_sensor(180)
        distLeft= self.get_average_distance(3)
        baseLen = 25
	if distRight > 10 and distLeft > 10:
	    blah=0

	elif distRight < 20 and distLeft < 20: 
	    print("level1")	
            if distRight > distLeft:
                perpendicularLen = (distRight - distLeft) / 2
                angleDisplacement = round(math.degrees(math.atan(perpendicularLen / baseLen)),0)
            elif distRight < distLeft:
                perpendicularLen = (distLeft - distRight) / 2
                angleDisplacement = round(math.degrees(math.atan(perpendicularLen / baseLen)),0)
            self.turn_degrees(angleDisplacement,300)
  
            for i in range (0,180,20):
                self.turn_distance_sensor(i)
                if self.current_distance.value < 10:
                    self.calibrateJunction()

	elif distRight < 20 and distLeft >20:
	    print ("level2")
	    self.turn_degrees(-20,300)

            for i in range (0,180,20):
                self.turn_distance_sensor(i)
                if self.current_distance.value < 10:
                    self.calibrateJunction()
	elif distRight > 20 and distLeft <20:
            print("level 3")
	    self.turn_degrees(20,300)

            for i in range (0,180,20):
                self.turn_distance_sensor(i)
                if self.current_distance.value < 10:
                    self.calibrateJunction()


	    
	
def main():
    #create class object(s)
    bot = SlaughterBot(4)

    bot.turn_distance_sensor(90)

    p = mp.Process(target=bot.read_continuous_distance)
    p.start()
    while True:
# 	pickChoice=bot.check_Crash()

#	if (pickChoice ==1):
#            bot.calibrateJunction()
	bot.move_distance(10)
        #scan for corridors
        angles = bot.scan_distance_angles(27, 90)
        x = len(angles)
        if x == 0:
            # Dead end ... reverse logic here - no where to go
            bot.turn_degrees(180,180)
            time.sleep(1)
            bot.turn_distance_sensor(90)
            time.sleep(0.25)
            continue
        
        bot.turn_distance_sensor(90)
	time.sleep(0.25)
	angle = random.choice(angles)
        print("Choices= ",angles)
        print("Picked= ",angle)
        #print("random angle=",angle)
        if angle < 90:
            degrees = 90 - angle
            bot.turn_distance_sensor(angle)
            time.sleep(0.5)
            #Find mid of the corridor and adjust
            bot.holeSubroutine(angle)
            #bot.move_distance(16)
        elif angle == 90:
            degrees = 0
            if x > 1:
                #print("x=", x)    #number of corridors
                bot.move_distance(28)
                time.sleep(2)
        else:
            degrees = angle - 270
            bot.turn_distance_sensor(angle)
            time.sleep(0.5)
            #Find mid of the corridor and adjust
            bot.holeSubroutine(angle)
            #bot.move_distance(16)

        #bot.calibrateJunction()
	bot.turn_distance_sensor(angle)
        time.sleep(0.25)
        
	
	bot.turn_degrees(degrees, 180)
        time.sleep(1)
        bot.turn_distance_sensor(90)
        time.sleep(0.25)
	
	#pickChoice=bot.check_Crash()

        #if (pickChoice ==1):
        #bot.calibrateJunction()

def init():
    bot = SlaughterBot(4)
    bot.turn_distance_sensor(90)
    p = mp.Process(target=bot.read_continuous_distance)
    p.start()
    return bot

def loop_test(bot):
    bot.move_distance(10)
    angles = bot.scan_distance_angles(20, 90)
    x = len(angles)
    if x == 0:
        # reverse logic here - no where to go
        bot.turn_degrees(180,90)
        return

    angle = random.choice(angles)
    print("angles: {} picked: {}".format(angles, angle))
    if angle < 90:
        degrees = 90 - angle
        bot.turn_distance_sensor(angle)
        bot.move_distance(16)
    elif angle == 90:
        degrees = 0
        if x > 1:
            print("x=", x)    #number of corridors
            bot.move_distance(28)
    else:
        degrees = angle - 270
        bot.turn_distance_sensor(angle)
        bot.move_distance(16)
    # let's see what direction we picked
    bot.turn_distance_sensor(angle)
    bot.turn_degrees(degrees, 90)
    bot.turn_distance_sensor(90)

if __name__ == "__main__":
    main()
