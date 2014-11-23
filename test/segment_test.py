import sys
sys.path.insert(0, 'src')
import unittest
from ddt import ddt, data#, file_data
#import cv2
import segment
#import numpy as np

@ddt
class TestSegmentation(unittest.TestCase):

    def test_segment(self):
    	image = None
    	tile_number = segment.tile_count(image)
    	self.assertEqual(1,tile_number)

    @data( ([0,5,10,13,25],[0,13,25]),
        ([0,15,23,26],[0,15,26]),
        ([0,15],[0,15]),
        ([0],[0]) )
    def test_grow(self,datapoint):
        data,expected = datapoint
        got = segment.grow(data,10)
        self.assertEqual(expected,got)
        
if __name__ == '__main__':
    unittest.main(verbosity=2)