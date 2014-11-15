import sys
sys.path.insert(0, 'src')
import unittest
from ddt import ddt, data
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

    @data(  \
       {"test_001.jpg": ((408,112),(150,295),(500,295),(160,500),(470,500),(720,500))},
       {"test_002.jpg": ((391,100),(134,264),(476,270),(143,462),(437,471),(692,474))},
       {"test_003.jpg": ((417,139),(160,300),(528,320),(166,505),(475,520),(720,520))},
       {"test_004.jpg": ((285,165),(675,230),(270,361),(700,350))},
       {"test_005.jpg": ((300,135),(140,286),(460,315),(116,477),(440,485),(710,484))},
       {"test_006.jpg": ((400,110),(700,130),(160,314),(460,300),(685,345),(431,516))},
       {"test_007.jpg": ((300,330),(675,375),(278,489),(692,502))} \
            )
    def test_inside_points(self, location_dict):
         file_name = str(location_dict.keys()[0])
         internal_points = np.array(location_dict.values()[0])
         image = cv2.imread("test/test_data/" + file_name)
         contours = detect_clusters.fetch_contours(image,100)
         got = [] #got[i] is true if any point is internal_points is in contours[i]
         for cnt in contours:
            is_in_contour = [] #element i is 1 (one) if cnt contains any point in internal_points
            for point in internal_points:
              is_in_contour.append(cv2.pointPolygonTest(cnt, tuple(point),False))
            got.append(1 in is_in_contour)
         self.assertNotIn(False,got)

if __name__ == '__main__':
    unittest.main(verbosity=2)
