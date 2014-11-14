import sys
sys.path.insert(0, 'src')
import unittest
from ddt import ddt, data
import cv2
import matplotlib.pyplot as plt
import detect_clusters

@ddt
class TestSequenceFunctions(unittest.TestCase):

    def open_sample(self, index):
        return cv2.imread("test/test_data/test_" + index + ".jpg")

    def test_open_sample(self):
        image = self.open_sample("001")
        self.assertNotEqual(image,None)

    @data((1,6),(2,6),(3,6),(4,4),(5,6),(6,6),(7,4))
    def test_count(self, datapoint):
        image_index, expected = datapoint
        image = self.open_sample( "00{}".format(image_index) )
        got = detect_clusters.count(image)
        self.assertEqual(expected, got)


if __name__ == '__main__':
    unittest.main(verbosity=2)
