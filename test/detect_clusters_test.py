import sys
sys.path.insert(0, 'src')
import unittest
import detect_clusters
import cv2
import matplotlib.pyplot as plt

class TestSequenceFunctions(unittest.TestCase):

    def open_sample(self, index):
        return cv2.imread("test/test_data/test_" + index + ".jpg")

    def test_open_sample(self):
        image = self.open_sample("001")
        self.assertNotEqual(image,None)

    def test_whatever(self):
        image = self.open_sample("001")
        clusters_count = detect_clusters.count( image )
        self.assertEqual(6, clusters_count)

if __name__ == '__main__':
    unittest.main()