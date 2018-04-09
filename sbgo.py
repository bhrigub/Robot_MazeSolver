# Slaughterbot Go scripts and API
import sys

sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy

class SlaughterBot():
    def __init__(self):
        self.gpg = easy.EasyGoPiGo3()
        self.distance_sensor = self.gpg.init_distance_sensor()
        self.servo = self.gpg.init_servo("SERVO2")
        
    #Get a single reading from the distance sensor.
    def read_single_distance(self):
            return self.distance_sensor.read_mm()


# Turn the distance sensor some number of degrees
# (specified by an argument) right/left
    def turn_distance_sensor(self, degrees):
        self.servo.rotate_servo(degrees)
    

    

# Turn wheel 1 or 2 forward or backward independently
# (this can be several functions, or a single function
# that takes arguments).
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


#Control the wheels together to turn the robot 90 degrees right/left

#Control the wheels together to t urn some number of degrees (specified by an argument)
#right/left

#Turn the wheels in order to move the robot a specified distance forward or back (in cm).

#Get a continuous stream of readings from the distance sensor.

#Read the en coders position, in degrees. (See
#github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py)
#Print the encoders positions in a continuous stream.
    def read_encoders(self):
        try:	    
            while True:
                print("Encoders positions in degrees (left motor, right motor): " + str(self.gpg.read_encoders()))
        except KeyboardInterrupt:
            self.gpg.reset_all()
	    self.gpg.reset_encoders() 
    

def main():
    # do stuff
    bot = SlaughterBot()
    # turn_distance_sensor
    #degrees = input("Enter degrees to rotate:: ")
    #bot.turn_distance_sensor(degrees)
    #turn wheels
    direction = input("Enter the direction:: ")
    bot.turn_wheels(direction)
    #read and print encoders
    bot.read_encoders()

if __name__ == "__main__":
    main()

