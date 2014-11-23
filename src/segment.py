import numpy as np
import cv2
import matplotlib.pyplot as plt

def tile_count(image):
	return 1

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

if __name__ == '__main__':
    test_data_path = 'test/test_data/'
    test_image = cv2.imread(test_data_path+'melds_001/segment_5.jpg')
    test_hsv = cv2.cvtColor(test_image, cv2.COLOR_BGR2HSV)
    test_value_img = test_hsv[:,:,2]
    #must integrate with scraps I have elsewhere    
    ret, val_mask = cv2.threshold(test_value_img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = np.ones((3,3),np.uint8) #the kernel size has to be adapted if we use smaller samples
    closed_enough = cv2.morphologyEx(val_mask, cv2.MORPH_CLOSE, kernel)
    #plt.imshow(closed_enough)
    maxvp,cols = np.shape(closed_enough)
    #maxvp = np.shape(test_value_img)[0]
    coldensity = np.array([np.count_nonzero(closed_enough[:,i]) for i in range(cols)])
    #plt.bar(range(width),coldensity)
    discriminant = (np.mean(coldensity) + np.min(coldensity))/2.0
    indexes = np.where(coldensity < discriminant)[0]
    clusters = onedcluster(indexes,10)
    divs = map(int,[np.median(group) for group in clusters if group != [] ])
    #incude origin
    divs.insert(0,0)
    #include end
    divs.append(cols-1)
    for x in divs:
        cv2.line(test_image,(x,0),(x,maxvp-1),(0,255,0),2)
    plt.imshow(test_image)
    plt.show()
    