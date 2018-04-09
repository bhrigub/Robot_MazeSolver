"""
@author: Achin, Bhrigu, Frank
References: https://github.com/DexterInd/GoPiGo3/blob/master/Software/Python/easygopigo3.py
"""
import unittest
import sbgo

class TestSBGo(unittest.TestCase):
    def setUp(self):
        self.bot = sbgo.SlaughterBot()

    def test_read_single_distance(self):
        reading = self.bot.read_single_distance()
        print("read_single_distance: {}".format(reading))
        self.assertTrue(isinstance(reading, int))
    def test_motor_movement (self):
        for i in range(0,10):
            if i < 5:
                if i % 2 == 1:
                    turn_wheels ("forward")
                    time.sleep (1)
                else:
                    turn_wheels ("backward")
                    time.sleep (1)
            else:
                if i % 2 == 1:
                    turn_wheels ("left")
                    time.sleep (1)
                else:
                    turn_wheels ("right")
                    time.sleep (1)
            
if __name__ == '__main__':
    unittest.main()
