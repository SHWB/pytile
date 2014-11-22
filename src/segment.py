import numpy as np
import cv2
import matplotlib.pyplot as plt

def tile_count(image):
	return 1

if __name__ == '__main__':
    test_data_path = 'test/test_data/'
    test_image = cv2.imread(test_data_path+'melds_001/segment_5.jpg')
    test_hsv = cv2.cvtColor(test_image, cv2.COLOR_BGR2HSV)
    test_value_img = test_hsv[:,:,2]
    #must integrate with scraps I have elsewhere
    