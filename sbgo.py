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
        self.current_direction = 'N'
        self.backtracking = False
        self.genList = list()
        self.visited = list()
        self.x = 0
        self.y = 0


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
        if self.current_distance.value > 9:
            # TODO: this can be moved outside
            self.turn_distance_sensor(90)
            if distance_val>10:
                while distance_val > 0:
                    travel = 5
		    self.calibration()
                    self.move_distance(travel)
                    distance_val = distance_val - 5
                    print("Distance travelled = ", travel)
                    print("Distance trailing = ", distance_val)
            else:
                start = self.read_encoders_avg("cm")
                target = start + distance_val
                print("start = " +str(start))
                print("target = "+str(target))
                self.gpg.drive_cm(distance_val, False)   
                time.sleep(2)
                print("Pos = "+str(self.read_encoders_avg("cm")))
                self.coordinateBuilder(start)


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
            print("scan_distance_angles: angle: {} distance: {}".format(i, distance))

            if distance > min_distance:
                angles.append(i)

            i += delta_angle
        self.turn_distance_sensor(90)
        return angles

    # Returns the average distance over len readings
    def get_average_distance(self, len):
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



    def sensorRead(self):
        self.turn_distance_sensor(0)
        dist0= self.get_average_distance(3)
        self.turn_distance_sensor(45)
        dist45= self.get_average_distance(3)
        self.turn_distance_sensor(90)
        dist90= self.get_average_distance(3)
        self.turn_distance_sensor(135)
        dist135= self.get_average_distance(3)
        self.turn_distance_sensor(180)
        dist180= self.get_average_distance(3)
        self.turn_distance_sensor(90)
        print ("Sensor reading",dist0, dist45, dist90, dist135, dist180)

        return dist0, dist45, dist90, dist135, dist180

    def calibration(self):

        distRight, dist45, dist90, dist135, distLeft= self.sensorRead()
        baseLen = 10
        nocalibration=0
        centerOfRotation =10
        baseDist = 28/2
        if distRight < 30 or  distLeft < 30:

            #if distRight > 10 and distLeft > 10:
            #    nocalibration=1

            if distRight < 30 and distLeft < 30:
                if distRight > distLeft:
                    perpendicularLen = (distRight - distLeft) / 2
                    #angleDisplacement = 10
                    angleDisplacement = round(math.degrees(math.atan(perpendicularLen / baseLen)))
                elif distRight < distLeft:
                    perpendicularLen = (distLeft - distRight) / 2
                    #angleDisplacement = -10
                    angleDisplacement = -(round(math.degrees(math.atan(perpendicularLen / baseLen))))
                else:
                    angleDisplacement = 0
                    print("Stuck at 1")
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision 1 picked: dist left <25 and dist right <25", angleDisplacement)
                
            elif distRight > 30 and distLeft < 14:
                hypotenLen = dist135
                perpendicularLen = centerOfRotation
                #angleDisplacement = round(math.degrees(math.asin(perpendicularLen/hypotenLen)))
                
                angleDisplacement = 12
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision 2 picked: dist left <10 and dist right > 25", angleDisplacement)
                
            elif distRight < 14 and distLeft > 30:
                hypotenLen = dist45
                perpendicularLen = centerOfRotation
                #angleDisplacement = -(round(math.degrees(math.asin(perpendicularLen/hypotenLen))))
                
                angleDisplacement = -12
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision 3 picked: dist left > 25 and dist right <10", angleDisplacement)
            elif dist45 > dist135:
                hypotenLen = dist135
                perpendicularLen = centerOfRotation
                #angleDisplacement = round(math.degrees(math.acos(perpendicularLen/hypotenLen)))
                
                #hypotenLen = centerOfRotation + dist135
                angleDisplacement = 12
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision Corner 4 picked: dist 45 is more", angleDisplacement)
                
            elif dist45 < dist135:
                hypotenLen = dist45
                perpendicularLen = centerOfRotation
                #angleDisplacement = -(round(math.degrees(math.asin(perpendicularLen/hypotenLen))))
                
                #hypotenLen = centerOfRotation + dist45
                angleDisplacement = -12
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision Corner 5 picked: dist 135 is more", angleDisplacement)
            else:
                time.sleep(0.5)
                print("stuck at 2")
                
        else:

            if dist45 > dist135:
                hypotenLen = dist135
                perpendicularLen = centerOfRotation
                #angleDisplacement = round(math.degrees(math.asin(perpendicularLen/hypotenLen)))                
                
                #hypotenLen = centerOfRotation + dist135
                angleDisplacement = 12
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision Corner 6 picked: dist 45 is more", angleDisplacement)

            elif dist45 < dist135:
                hypotenLen = dist45
                perpendicularLen = centerOfRotation
                #angleDisplacement = -(round(math.degrees(math.asin(perpendicularLen/hypotenLen))))
                
                #hypotenLen = centerOfRotation + dist45
                angleDisplacement = -12
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision Corner 7 picked: dist 135 is more", angleDisplacement)
            else:
                time.sleep(0.5)
                print("stuck at 3")

        if (dist45 <10 or dist135 < 10) and (distRight > 30) and (distLeft > 30):
            if dist45 > dist135:
                hypotenLen = dist135
                perpendicularLen = centerOfRotation
                #angleDisplacement = round(math.degrees(math.asin(perpendicularLen/hypotenLen)))          
                
                #hypotenLen = centerOfRotation + dist135
                angleDisplacement = 12
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision Corner 8 picked: dist 45 is more", angleDisplacement)
            elif dist45 < dist135:
                hypotenLen = dist135
                perpendicularLen = centerOfRotation
                #angleDisplacement = -(round(math.degrees(math.asin(perpendicularLen/hypotenLen))))
                
                #hypotenLen = centerOfRotation + dist45
                angleDisplacement = -12
                #angleDisplacement = round(math.degrees(math.acos(baseDist/hypotenLen)))
                self.turn_degrees(angleDisplacement,300)
                time.sleep(0.5)
                print("Descision Corner 9 picked: dist 135 is more", angleDisplacement)
            else:
                time.sleep(0.5)
                print("Stuck at 4")


        if nocalibration == 0:
            dist0, dist45, dist90, dist135, dist180= self.sensorRead()

            if dist0 < 10 or dist45 < 10 or dist90 < 10 or dist135 < 10 or dist180 < 10:
                self.calibration()
                time.sleep(0.5)

    def reverse_direction(self, direction):
        if direction == 'N':
            return 'S'
        elif direction == 'S':
            return 'N'
        elif direction == 'E':
            return 'W'
        elif direction == 'W':
            return 'E'

    def add_decision_point(self, decision_point):
	#add decision point to general list and mark as visited
        self.genList.insert(0, decision_point)

    def turn(self, angle, num_corridors):

        if angle < 90:
            degrees = 90 - angle
            self.turn_distance_sensor(angle)
            self.move_distance(14)
        elif angle == 90:
            degrees = 0
            if num_corridors > 1:
                print("turn: num_corridors =", num_corridors)
                self.move_distance(28)
        else:
            degrees = angle - 270
            self.turn_distance_sensor(angle)
            self.move_distance(14)

        self.turn_distance_sensor(angle)
        self.turn_degrees(degrees, 90)
        # update current direction
        self.update_direction(angle)
        self.turn_distance_sensor(90)
        self.move_distance(10)

    def update_direction(self, angle):
        self.current_direction = self.get_direction(angle)

    def get_direction(self, angle):
        # TODO: get smarter about this - make an array or table
        if angle == 0:
            if self.current_direction == 'N':
                return 'E'
            elif self.current_direction == 'E':
                return 'S'
            elif self.current_direction == 'S':
                return 'W'
            elif self.current_direction == 'W':
                return 'N'

        elif angle == 180:
            if self.current_direction == 'N':
                return 'W'
            elif self.current_direction == 'E':
                return 'N'
            elif self.current_direction == 'S':
                return 'E'
            elif self.current_direction == 'W':
                return 'S'

        else:
            return self.current_direction


    def get_choices(self, angles):
        choices = []
        for angle in angles:
            choices.append(self.get_direction(angle))
        return choices

    def cardinal_to_degrees(self, directionTo):
        d1 = self.current_direction
        d2 = directionTo

        if d1 == 'N':
            if d2 == 'E':
                angle = 0
            elif d2 == 'W':
                angle = 180
        elif d1 == 'E':
            if d2 == 'S':
                angle = 0
            elif d2 == 'N':
                angle = 180
        elif d1 == 'W':
            if d2 == 'N':
                angle = 0
            elif d2 == 'S':
                angle = 180
        elif d1 == 'S':
            if d2 == 'W':
                angle = 0
            elif d2 == 'E':
                angle = 180

        if d1 == d2:
            angle = 90

        return angle

    def turn_cardinal(self, directionTo):
        reverse = self.reverse_direction(self.current_direction)
        if directionTo == reverse:
            self.turn_degrees(180, 90)
            self.current_direction = reverse
        else:
            angle = self.cardinal_to_degrees(directionTo)
            self.turn(angle, 1)

    def navigate(self):
        # get latest decision point
        if len(self.genList) > 0:
            dp = self.genList[0]

            # if backtracking, turn back to initial direction
            if self.backtracking == True:
                self.turn_cardinal(dp.initial_direction)
                print("navigate: I'm not backtracking anymore!")

            # get unexplored direction of that decision point
            if len(dp.choices) > 0:
                direction = dp.choices.pop()
                if (self.current_direction != direction):
                    self.turn_cardinal(direction)
                else:
                    print("navigation: I picked {} and I'm already going {}".format(self.current_direction, direction))
            # if no more directions, turn around and head toward prior dp
            else:
                self.turn_cardinal(self.reverse_direction(dp.initial_direction))
                self.visited.append(dp)
                self.genList.pop(0)
                self.backtracking = True
                print("navigate: backtracking!")
            print("navigate: I am heading: {}".format(self.current_direction))
        else:
            print("navigate: I have no more nodes to explore!")    

    #Map coordinates as robot moves around
    def coordinateBuilder(self, start):
        x = 0
        y = 0
	print("Current_direction: ",self.current_direction)
        if self.current_direction == 'N':
            y = self.read_encoders_avg("cm")
        elif self.current_direction == 'E':
            x = self.read_encoders_avg("cm")
        elif self.current_direction == 'W':
            x = -(self.read_encoders_avg("cm"))
        else:
            y = -(self.read_encoders_avg("cm"))
        print("Add x: {}, Add y: {}".format(x,y)) 
        #Calculate actual distance travelled
        if x!=0 and x>0:
            x = x - start
        if x < 0:
            x = x + start
        if y!=0 and y>0:
            y = y - start
        if y < 0:
            y = y + start
        print("Coordinates traversed:: u= {}; v= {} ".format(str(x),str(y)))
        #Calculate current coordinates
        self.x = self.x + x
        self.y = self.y + y 
        print("Current Coordinates:: x= {}; y= {} ".format(str(self.x),str(self.y)))
        
        #return self.x, self.y 

class DecisionPoint:
    """
    initial_direction: the direction the robot is facing when first approaching
        the decision point - one of N,S,E,W
    x: the x grid location
    y: the y grid location
    choices: the directions available to move from this decision point - array
        of [N,S,E,W]
    """
    def __init__(self, initial_direction, x, y, choices):
        self.initial_direction = initial_direction
        self.x = x
        self.y = y
        self.choices = choices

def main():
    #create class object(s)
    bot = SlaughterBot(4)

    bot.turn_distance_sensor(90)

    #bot.calibration()

    p = mp.Process(target=bot.read_continuous_distance)
    p.start()
    while True:
        print("current direction: {}".format(bot.current_direction))
        bot.calibration()
#       pickChoice=bot.check_Crash()

#	if (pickChoice ==1):
#            bot.calibrateJunction()
        time.sleep(1)
        # TODO: We might start at a decision point, so we should probably scan first before moving
        bot.move_distance(10)
        #scan for corridors
        angles = bot.scan_distance_angles(30, 90)
        x = len(angles)
        if x == 0:
            # Dead end ... reverse logic here - no where to go
            bot.turn_degrees(180,90)
            # TODO: we can make this function call turn degrees 180,90
            bot.current_direction = bot.reverse_direction(bot.current_direction)
            print("main: I am backtracking!!")
            bot.backtracking = True
            time.sleep(1)
            continue

        elif x == 1:
            # turn that direction
            bot.turn(angles[0], x)

        else:
            if bot.backtracking == False:
                # expansion
                # turn angles into N,S,E,W choices
                choices = bot.get_choices(angles)
                # more than one direction, so make decision point
                dp = DecisionPoint(bot.current_direction, bot.x, bot.y, choices)
                # add decision point to stack
                bot.add_decision_point(dp)

	    # move phase
	    # pick direction to move based on stack decision point
	    # TODO: print direction we're trying in navigate
            bot.navigate()


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
        degrees = 90 - angle
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
