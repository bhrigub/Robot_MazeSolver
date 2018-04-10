# Slaughterbot Go scripts and API
# Authors: A, B, F
# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
import multiprocessing as mp

import sys
import time

sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy

class SlaughterBot():
    def __init__(self, distance_hz=0):
        self.gpg = easy.EasyGoPiGo3()
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

if __name__ == "__main__":
    main()
