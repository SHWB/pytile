import sys
sys.path.insert(0, 'src')
import unittest
import detect_clusters
import cv2
import matplotlib.pyplot as plt

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.dataset_expected_clusters_count = [6,6,6,4,6,6,4]

    def open_sample(self, index):
        return cv2.imread("test/test_data/test_" + index + ".jpg")

    def test_open_sample(self):
        image = self.open_sample("001")
        self.assertNotEqual(image,None)

    def test_count(self):
        clusters_count = []
        for i in range(1,8):
            image = self.open_sample( "00{}".format(i) )
            clusters_count.append( detect_clusters.count(image) )
        self.assertEqual(self.dataset_expected_clusters_count, clusters_count)


if __name__ == '__main__':
    unittest.main(verbosity=2)
