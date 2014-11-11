# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 18:47:25 2014

@author: shwb
"""

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
hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
himg = hsvimg[:,:,0]
simg = hsvimg[:,:,1]
#%%
"""
thresholding seems more effective if done on blurred images
the candidate zones are characterized by low Hue and very low Saturation
"""
blurh = cv2.GaussianBlur(cv2.equalizeHist(simg),(5,5),0)
blurs = cv2.GaussianBlur(himg,(5,5),0)
#H channel is in range [0,175]
reth, maskh = cv2.threshold(blurh,60,175,cv2.THRESH_BINARY_INV)
rets, masks = cv2.threshold(blurs,50,255,cv2.THRESH_BINARY_INV)
msk = cv2.bitwise_and(maskh,masks)
#%%
#apply closing in order to remove 'holes' in our tiles
kernel = np.ones((15,15),np.uint8)
closed = cv2.morphologyEx(msk, cv2.MORPH_CLOSE, kernel)
#%%
ctrlen = 500
#find the countours
contours, hier = cv2.findContours(closed,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
i=0
for cnt in contours:
    if cv2.arcLength(cnt,True) > ctrlen:
        (x,y,w,h) = cv2.boundingRect(cnt)
        tmpim = img[y:y+h,x:x+w]
        i+=1
        cv2.imwrite(str('segment'+str(i)+'.jpg'),tmpim)
        cv2.rectangle(cpy,(x,y),(x+w,y+h),(0,255,0),3)
#%%
plt.imshow(cpy,'gray')
plt.show()        
#%%


