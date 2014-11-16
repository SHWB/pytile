import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from math import sin, pi

def count(image):
    contours,l = fetch_contours(image,100)
    return len(contours)

def fetch_contours(image, min_length):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    val_channel = hsv[:,:,2]
    retv, val_mask = cv2.threshold(val_channel,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    #apply closing in order to remove 'holes' in our tiles
    kernel = np.ones((7,7),np.uint8) #the kernel size has to be adapted if we use smaller samples
    closed_enough = cv2.morphologyEx(val_mask, cv2.MORPH_CLOSE, kernel)
    """
    Find contours in each candidate region.
    We use RETR_EXTERNAL because we're not interested in inner sub-regions
    """
    contours, hier = cv2.findContours(closed_enough,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    """
    Avoid counting contours that surely don't belong to a tile.
    I noticed a value channel based approach is sensible to noise and creates many 0 length contours.
    This explains the condition in the returned list:
    at the resolution we're working at a tile contour should be certainly larger than 100 pixels.
    """
    candidate_contours = np.array([contour for contour in contours if cv2.arcLength(contour,True) > min_length])
    candidate_contours_lengths = np.array([cv2.arcLength(candidate, True) for candidate in candidate_contours])
    return candidate_contours, candidate_contours_lengths

def get_winning_tile(contours,lengths):
    winning_tile_index = np.argmin(lengths)
    return contours[winning_tile_index]

def is_somewhat_straight(angle,tolerance):
    # all quantities in degrees
    return abs(sin(pi/90*angle)) <= sin(pi/90*tolerance)

def straighten(image,angle,tolerance=4):
    """
    Rotate melds that are not orthogonal within the tolerance(degrees)
    """
    if is_somewhat_straight(angle,tolerance):
        return image
    else:
        rows,cols,channel = image.shape
        #cv2.getRotationMatrix2D(center,angle,scale), the angle is CCW
        M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
        rotated = cv2.warpAffine(image,M,(cols,rows))
        return rotated

if __name__ == '__main__':
    for sample_index in range(1,8):
        image = cv2.imread('test/test_data/test_00{}.jpg'.format(sample_index))
        contours, lengths = fetch_contours(image,100) #min_length should be tuned on image size
        if contours.size == 0:
            break
        segment_index = 1
        test_data_path = 'test/test_data/'
        melds_dir = 'melds_00{}'.format(sample_index)
        winning_tile_index = np.argmin(lengths)
        if not os.path.exists(test_data_path + melds_dir):
            os.makedirs(test_data_path + melds_dir)
        for contour_index in range(len(contours)):
            (x,y,w,h) = cv2.boundingRect(contours[contour_index])
            # rotated_box = cv2.fitEllipse(contours[contour_index]) # <-- this doesn't work very well
            rotated_box = cv2.minAreaRect(contours[contour_index])
            #rotated_box: Box2D structure - ( top-left corner(x,y), (width, height), clockwise angle of rotation )
            bounded_meld = image[y:y+h,x:x+w]
            if contour_index != winning_tile_index:
                segment_out = straighten(bounded_meld,rotated_box[2])
                cv2.imwrite(test_data_path + melds_dir + '/segment_{}.jpg'.format(segment_index), segment_out)
            else:
                rows,cols,channel = bounded_meld.shape
                CCW_rotation = cv2.getRotationMatrix2D((cols/2,rows/2),-90,1)
                segment_out = straighten(bounded_meld,rotated_box[2])
                segment_out = cv2.warpAffine(segment_out,CCW_rotation,(cols,rows))
                cv2.imwrite(test_data_path + melds_dir + '/single_segment_{}.jpg'.format(segment_index), segment_out)
            segment_index += 1
