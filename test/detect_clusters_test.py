import sys
sys.path.insert(0, 'src')
import unittest
from ddt import ddt, data, file_data
import cv2
import detect_clusters
import numpy as np

@ddt
class TestDetection(unittest.TestCase):

    @data((1,6),(2,6),(3,6),(4,4),(5,6),(6,6),(7,4))
    def test_count(self, datapoint):
        image_index, expected = datapoint
        image = cv2.imread("test/test_data/test_00{}.jpg".format(image_index))
        got = detect_clusters.count(image)
        self.assertEqual(expected, got)

    @file_data('test_data/melds_locations.json')
    def test_inside_points(self, location_dict):
         file_name = str(location_dict.keys()[0])
         internal_points = np.array(location_dict.values()[0])
         image = cv2.imread("test/test_data/" + file_name)
         contours = detect_clusters.fetch_contours(image,100)
         got = [] #got[i] is true if any point in internal_points is in contours[i]
         for cnt in contours:
            is_in_contour = [] #element i is 1 (one) if cnt contains any point in internal_points
            for point in internal_points:
              is_in_contour.append(cv2.pointPolygonTest(cnt, tuple(point),False))
            got.append(1 in is_in_contour)
         self.assertNotIn(False,got)

if __name__ == '__main__':
    unittest.main(verbosity=2)
