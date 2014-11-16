import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from math import sin, pi

def count(image):
    contours = fetch_contours(image,100)
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
    return np.array([contour for contour in contours if cv2.arcLength(contour,True) > min_length])

def rotate(image,angle,tolerance=5):
    """
    At the moment we obtain melds which are not orthogonal.
    Need to rotate them if too crooked
    """
    if is_somewhat_straight(angle,tolerance):
        return image
    else:
        rows,cols = image.shape
        #cv2.getRotationMatrix2D(center,angle,scale)
        M = cv2.getRotationMatrix2D((cols/2,rows/2),-angle,1)
        dst = cv2.warpAffine(image,M,(cols,rows))
        return dst

def is_somewhat_straight(angle,tolerance):
    # all quantities in degrees
    return abs(sin(pi/90*angle)) <= sin(pi/90*tolerance)


if __name__ == '__main__':
    for i in range(1,8):
        image = cv2.imread('test/test_data/test_00{}.jpg'.format(i))
        contours = fetch_contours(image,100) #min_length should be tuned on image size
        if contours.size == 0:
            break
        j = 1
        test_data_path = 'test/test_data/'
        melds_dir = 'melds_00{}'.format(i)
        if not os.path.exists(test_data_path + melds_dir):
            os.makedirs(test_data_path + melds_dir)
        for cnt in contours:
            (x,y,w,h) = cv2.boundingRect(cnt)
            rect = cv2.minAreaRect(cnt)
            #rect: Box2D structure - ( top-left corner(x,y), (width, height), clockwise angle of rotation )
            meld = image[y:y+h,x:x+w]
            segment_out = rotate(meld,rect)
            cv2.imwrite(test_data_path + melds_dir + '/segment_{}.jpg'.format(j), segment_out)
            j += 1
