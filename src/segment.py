# -*- coding: utf-8 -*-
"""
Created on Sun Nov  9 22:40:38 2014

@author: shwb
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2

def onedcluster(array,tol):
    clusters = [[]]
    j = 0
    for i in range(len(array)-1):
        if (array[i+1] - array[i]) < tol:
            clusters[j].append(array[i])
        else:
            clusters.append([])
            j+=1  
    return clusters

#%%
img = cv2.imread('segment3.jpg')
seg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, th= cv2.threshold(cv2.equalizeHist(seg),75,255,cv2.THRESH_BINARY_INV)
#%%
width = np.shape(th)[1]
coldensity = np.array([np.count_nonzero(th[:,i]) for i in range(width)])
#plt.bar(range(width),coldensity)
#%%
indexes = np.where(coldensity < 20)[0]
clusters = onedcluster(indexes,4)

divs = map(int,[np.median(group) for group in clusters if group != [] ])
#%%
maxvp = np.shape(seg)[1]-1
for x in divs:
    cv2.line(img,(x,0),(x,maxvp),(0,255,0),2)

plt.imshow(img,'gray')
plt.show()

