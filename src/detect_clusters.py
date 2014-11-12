import numpy as np
import cv2

def count(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue_channel = hsv[:,:,0]
    #H channel is in range [0,175]
    reth, hue_mask = cv2.threshold(hue_channel,0,175,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    #%%
    #apply closing in order to remove 'holes' in our tiles
    kernel = np.ones((7,7),np.uint8) #the kernel size has to adapted if we use smaller samples
    closed_enough = cv2.morphologyEx(hue_mask, cv2.MORPH_CLOSE, kernel)
    #%%
    """
    find contours in every candidate region.
    We user RETR_EXTERNAL because we're not interested in inner sub-regions
    """
    contours, hier = cv2.findContours(closed_enough,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)
