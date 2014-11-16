import sys
sys.path.insert(0, 'src')
import unittest
from ddt import ddt, data, file_data
import cv2
import segment
import numpy as np

@ddt
class TestSegmentation(unittest.TestCase):

    def test_segment(self):
    	image = None
    	tile_number = segment.tile_count(image)
    	self.assertEqual(1,tile_number)

if __name__ == '__main__':
    unittest.main(verbosity=2)