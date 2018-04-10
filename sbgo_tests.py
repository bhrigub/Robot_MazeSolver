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

if __name__ == '__main__':
    unittest.main()
