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
         contours, l = detect_clusters.fetch_contours(image,100)
         got = [] #got[i] is true if any point in internal_points is in contours[i]
         for cnt in contours:
            is_in_contour = [] #element i is 1 (one) if cnt contains any point in internal_points
            for point in internal_points:
              is_in_contour.append(cv2.pointPolygonTest(cnt, tuple(point),False))
            got.append(1 in is_in_contour)
         self.assertNotIn(False,got)

    @file_data('test_data/winner_locations.json')  
    def test_winner_locations(self,location_dict):
        file_name = str(location_dict.keys()[0])
        win_center = np.array(location_dict.values()[0])
        image = cv2.imread('test/test_data/'+file_name)
        contours, l = detect_clusters.fetch_contours(image,100)
        win_tile_contour = detect_clusters.get_winning_tile(contours,l)
        got = (1 == cv2.pointPolygonTest(win_tile_contour,tuple(win_center),False))
        self.assertTrue(got)

    @data((3,True),(0,True),(-4,True),(140,False),(271,True),(-45,False))
    def test_is_somewhat_straight(self,datapoint):
        angle,expected = datapoint
        got = detect_clusters.is_somewhat_straight(angle,5)
        self.assertEqual(expected,got)

if __name__ == '__main__':
    unittest.main(verbosity=2)
