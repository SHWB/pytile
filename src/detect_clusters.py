import numpy as np
import cv2

def count(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue_channel = hsv[:,:,0]
    sat_channel = hsv[:,:,1]
    #%%
    """
    thresholding seems more effective if done on blurred images
    the candidate zones are characterized by low Hue and very low Saturation
    """
    blurred_sat_channel = cv2.GaussianBlur(sat_channel,(5,5),0)
    blurred_hue_channel = cv2.GaussianBlur(hue_channel,(5,5),0)
    #H channel is in range [0,175]
    reth, hue_mask = cv2.threshold(blurred_hue_channel,50,175,cv2.THRESH_BINARY_INV)
    rets, sat_mask = cv2.threshold(blurred_sat_channel,60,255,cv2.THRESH_BINARY_INV)
    mask = cv2.bitwise_and(hue_mask,sat_mask)
    #%%
    #apply closing in order to remove 'holes' in our tiles
    kernel = np.ones((15,15),np.uint8)
    closed_enough = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #%%
    #find the countours
    contours, hier = cv2.findContours(closed_enough,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)