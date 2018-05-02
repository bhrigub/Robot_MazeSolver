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
        time.sleep(0.25)


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
        if self.current_distance.value > 20:
            self.turn_distance_sensor(90)
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
        #self.gpg.set_motor_limits(self.gpg.MOTOR_LEFT + self.gpg.MOTOR_RIGHT, dps = 90)

        # Set each motor target
        self.gpg.set_motor_position(self.gpg.MOTOR_LEFT, (StartPositionLeft + WheelTurnDegrees))
        self.gpg.set_motor_position(self.gpg.MOTOR_RIGHT, (StartPositionRight - WheelTurnDegrees))
        time.sleep(1)

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

    #def holeFinder (self, angle):


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

#Function Objective: Sense the environment around the robot
#Input Strings: None
#Default Action: None
#Output: Distance at 0, 45, 90, 135, 180 degrees

    def sensorRead(self):
        self.turn_distance_sensor(0)
        #time.sleep(0.15)
        dist0= self.get_average_distance(3)
        time.sleep(0.10)
        self.turn_distance_sensor(45)
        #time.sleep(0.15)
        dist45= self.get_average_distance(3)
        time.sleep(0.10)
        self.turn_distance_sensor(90)
        #time.sleep(0.15)
        dist90= self.get_average_distance(3)
        time.sleep(0.10)
        self.turn_distance_sensor(135)
        #time.sleep(0.15)
        dist135= self.get_average_distance(3)
        time.sleep(0.10)
        self.turn_distance_sensor(180)
        #time.sleep(0.15)
        dist180= self.get_average_distance(3)
        time.sleep(0.10)
        self.turn_distance_sensor(90)
        time.sleep(0.25)
        print ("Sensor reading",dist0, dist45, dist90, dist135, dist180)

        return dist0, dist45, dist90, dist135, dist180

#Function Objective: Calibrate the robot according to the environment
#Input Strings: None
#Default Action: None
#Output: Distance at 0, 45, 90, 135, 180 degrees

    def calibration(self):

        distRight, dist45, dist90, dist135, distLeft= self.sensorRead()
        baseLen = 10
        nocalibration=0
        centerOfRotation =10
        baseDist = 28/2
        if distRight < 25 or  distLeft < 25:

            #if distRight > 10 and distLeft > 10:
            #    nocalibration=1

            if distRight < 25 and distLeft < 25:
                if distRight > distLeft:
                    perpendicularLen = (distRight - distLeft) / 2
                    angleDisplacement = 13
                    #angleDisplacement = round(math.degrees(math.atan(perpendicularLen / baseLen)))
                elif distRight < distLeft:
                    perpendicularLen = (distLeft - distRight) / 2
                    angleDisplacement = -13
                    #angleDisplacement = -(round(math.degrees(math.atan(perpendicularLen / baseLen))))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.25)
                print("Descision 1 picked: dist left <25 and dist right <25", angleDisplacement)

            elif distRight > 25 and distLeft < 10:
                angleDisplacement = 13
                #angleDisplacement = round(math.degrees(math.atan(perpendicularLen / baseLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.25)
                print("Descision 2 picked: dist left <10 and dist right > 25", angleDisplacement)



            elif distRight < 10 and distLeft > 25:
                angleDisplacement = -13
                #angleDisplacement = round(math.degrees(math.atan(perpendicularLen / baseLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.25)
                print("Descision 3 picked: dist left > 25 and dist right <10", angleDisplacement)
            else:
                time.sleep(0.25)


        else:

            if dist45 > dist135:
                hypotenLen = centerOfRotation + dist135
                angleDisplacement = 13
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.25)
                print("Descision Corner 4 picked: dist 45 is more", angleDisplacement)

            elif dist45 < dist135:
                hypotenLen = centerOfRotation + dist45
                angleDisplacement = -13
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(-angleDisplacement,300)
                time.sleep(0.25)
                print("Descision Corner 5 picked: dist 135 is more", angleDisplacement)
            else:
                time.sleep(0.25)

        if dist45 <10 or dist135 < 10:
            if dist45 > dist135:
                hypotenLen = centerOfRotation + dist135
                angleDisplacement = 13
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.25)
                print("Descision Corner 4 picked: dist 45 is more", angleDisplacement)
            elif dist45 < dist135:
                hypotenLen = centerOfRotation + dist45
                angleDisplacement = -13
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(-angleDisplacement,300)
                time.sleep(0.25)
                print("Descision Corner 5 picked: dist 135 is more", angleDisplacement)
            else:
                time.sleep(0.25)


        if nocalibration == 0:
            dist0, dist45, dist90, dist135, dist180= self.sensorRead()

            if dist0 < 10 or dist45 < 10 or dist90 < 10 or dist135 < 10 or dist180 < 10:
                self.calibration()
                time.sleep(0.25)

#Global variable declaration for mapping
maze_Map = []
decision_Point = []
grid_Xaxis = 20
grid_Yaxis = 20
previous_Encoder = 0
previous_Direction = 'NA'
current_Direction = 'NA'

def mapping(self):
    global maze_Map, grid_Xaxis, grid_Yaxis, previous_Encoder, previous_Turn
    encoderValue = read_encoders_avg ('cm')

    distanceMoved = encoderValue - previous_Encoder
    if distanceMoved >= 10:
        if previous_Turn == 'NA':
            if previous_Encoder == 0:
                maze_Map.append(())








def main():
    #create class object(s)
    bot = SlaughterBot(4)

    bot.turn_distance_sensor(90)

    #bot.calibration()

    p = mp.Process(target=bot.read_continuous_distance)
    p.start()
    while True:
        bot.calibration()
#       pickChoice=bot.check_Crash()

#	if (pickChoice ==1):
#            bot.calibrateJunction()
	time.sleep(1)
        bot.move_distance(10)
        #scan for corridors
        angles = bot.scan_distance_angles(25, 90)
        x = len(angles)
        if x == 0:
            # Dead end ... reverse logic here - no where to go
            bot.turn_degrees(180,180)
            time.sleep(1)
            continue

        #bot.turn_distance_sensor(90)
	#time.sleep(0.25)
	angle = random.choice(angles)
        print("Choices= ",angles)
        print("Picked= ",angle)
        print("random angle=",angle)
        if angle < 90:
            degrees = 90 - angle
            bot.turn_distance_sensor(angle)
            time.sleep(0.5)

            #Find mid of the corridor and adjust
            #bot.holeSubroutine(angle)
            bot.move_distance(16)
        elif angle == 90:
            degrees = 0
            if x > 1:
                print("x=", x)    #number of corridors
                bot.move_distance(18)
                time.sleep(2)
        else:
            degrees = angle - 270
            bot.turn_distance_sensor(angle)
            time.sleep(0.5)
            #Find mid of the corridor and adjust
            #bot.holeSubroutine(angle)
            bot.move_distance(16)

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
    angles = bot.scan_distance_angles(20, 45)
    if len(angles) == 0:
        # reverse logic here - no where to go
        return

    angle = random.choice(angles)
    print("angles: {} picked: {}".format(angles, angle))
    if angle < 90:
        degr ees = 90 - angle
    elif angle == 90:
        degrees = 0
    else:
        degrees = angle - 270
    # let's see what direction we picked
    bot.turn_distance_sensor(angle)
    time.sleep(0.25)
    bot.turn_degrees(degrees, 90)
    time.sleep(1)
    bot.turn_distance_sensor(90)
    time.sleep(0.25)

if __name__ == "__main__":
    main()
