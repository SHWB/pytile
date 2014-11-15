import numpy as np
import cv2

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


