import sys
sys.path.insert(0, 'src')
import unittest
from ddt import ddt, data, file_data
import cv2
import segment


@ddt
class TestSegmentation(unittest.TestCase):

	@file_data('test_data/melds_tile_count.json')
    def test_segment(self):
    	image = None
    	tile_number = segment.tile_count(image)
    	self.assertEqual(0,tile_number)

if __name__ == '__main__':
    unittest.main(verbosity=2)