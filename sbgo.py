# Slaughterbot Go scripts and API
# Authors: A, B, F
# Attribution: code used from GoPiGo3 software found at:
# https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
import sys
import time

sys.path.append('/home/pi/Dexter/GoPiGo3/Software/Python')

import easygopigo3 as easy
import multiprocessing as mp

class SlaughterBot():
    def __init__(self, distance_hz=1):
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
        delay = 1.0/self.distance_hz
	    try:
            while True:
		        self.current_distance = self.read_single_distance()
		        print("Current distance: {}".format(self.current_distance))
                sleep(delay)
        except KeyboardInterrupt:
            self.gpg.reset_all()
	

def main():
    bot = SlaughterBot(4)
    p = mp.Process(target=bot.read_continuous_distance)
    p.start()
    p.join()

if __name__ == "__main__":
    main()
