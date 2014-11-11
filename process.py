# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 12:48:04 2014

@author: shwb
"""
#%%
import numpy as np
import cv2
import matplotlib.pyplot as plt
#%%
ori = cv2.imread('test.jpg')
r = ori.shape[0]/float(ori.shape[1])
DIM = (800, int(800*r))

#preprocess image
img = cv2.resize(ori,DIM,interpolation=cv2.INTER_AREA)
cpy = img.copy()
grayimg =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
"""
thresholding seems more effective if done on blurred images
"""
blur = cv2.GaussianBlur(cv2.equalizeHist(grayimg),(5,5),0)
ret, th = cv2.threshold(blur,190,255,cv2.THRESH_BINARY)

#%%
#apply closing in order to remove 'holes' in our tiles
kernel = np.ones((15,15),np.uint8)
closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
#%%
"""
a check on countours is needed because we want to find large areas
values are based on the image size
A check on the perimeter length is imo faster, but I didn't profile it
"""
ctrarea = 800*600*0.1 #not actually used
ctrlen = 500
#find the countours
contours, hierarchy = cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.arcLength(cnt,True) > ctrlen:
        (x,y,w,h) = cv2.boundingRect(cnt)
        cv2.rectangle(cpy,(x,y),(x+w,y+h),(0,255,0),3)

#%%
"""
epsilons = [0.1*cv2.arcLength(cnt,True) for cnt in contours]
approxes = [cv2.approxPolyDP(contours[i],epsilons[i],True) \
            for i in range(len(epsilons))]

for approx in approxes:
    cv2.drawContours(img, approx, -1, (0,255,0), 3)
"""
#eps = 0.1*cv2.arcLength(contours[10],True)
#approx = cv2.approxPolyDP(contours[10],eps,True)

#cv2 = cv2.drawContours(cpy,contours[],-1,(0,255,0),3)

plt.imshow(cpy,'gray')
plt.show()
