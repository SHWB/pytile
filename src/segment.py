import numpy as np
import cv2
import matplotlib.pyplot as plt

def tile_count(image):
    return 1

def onedcluster(array,tol):
    """
    returns an array of clusters (as list of lists). Two elements in the input
    array belong to the same monodimensional cluster if their difference is less
    than the tolerance tol
    """
    clusters = [[]]
    j = 0
    for i in range(len(array)-1):
        if abs(array[i+1] - array[i]) < tol:
            clusters[j].append(array[i])
        else:
            clusters.append([])
            j+=1  
    return clusters
    
def produce_segments(image):
    test_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    test_value_img = test_hsv[:,:,2] #working on the value channel, as always   
    #we're doing the same exact thresholding and closure thingy we did in detection
    ret, val_mask = cv2.threshold(test_value_img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    kernel = np.ones((3,3),np.uint8) #the kernel size has to be adapted if we use smaller samples
    closed_enough = cv2.morphologyEx(val_mask, cv2.MORPH_CLOSE, kernel)
    rows,cols = np.shape(closed_enough)
    #we count how many non-zero (aka black in the value space) pixels there are in each column
    coldensity = np.array([np.count_nonzero(closed_enough[:,i]) for i in range(cols)])
    """
    we need a way to detect 'valleys' in our coldensity plot: this is made by 
    choosing a discriminant value beneath of which lay all the intermediate zones
    of our tiles. This produces an array of indexes that are divided into clusters.
    """ 
    discriminant = (np.mean(coldensity) + np.min(coldensity))/2.0
    indexes = np.where(coldensity < discriminant)[0]
    clusters = onedcluster(indexes,int(.1*cols))
    #for each non-empty cluster found the median element is our candidate tile separator
    divs = map(int,[np.median(group) for group in clusters if group != [] ])
    
    #incude origin
    divs.insert(0,0)
    #include end
    divs.append(cols-1)
    return divs
    
def grow(array,tolerance):
    if len(array) < 2:
        return array
    i = 0
    #for each division, if the segmentation is too narrow, aggregate it with the
    #previous one
    while (i < len(array)-2): #don't check the last couple for reasons explained later
        if abs(array[i+1]-array[i]) <= tolerance:
            del array[i+1]
        else:
            i+=1
    #I couldn't think of a way to include this into a loop, because the last segment
    #has to be merged on the left rather than on the right
    if abs(array[-1]-array[-2]) <= tolerance:
        del array[-2]        
    return array

if __name__ == '__main__': #experiments I'm doing to come up with something
    test_data_path = 'test/test_data/'
    test_image = cv2.imread(test_data_path+'melds_001/segment_5.jpg')
    rows,cols,channels = test_image.shape
    divs = produce_segments(test_image)
    """
    divs may contain too many subclusters which may not correctly detect a tile. 
    We now have to aggregate clusters that are too narrow to legitimately be a tile:
    this is done simply evaluating the difference between consecutive 
    segmentation coordinates.
    """
    exp_tile_width = .33*rows
    divs = grow(divs,exp_tile_width)
    """    
    for x in divs:
        cv2.line(test_image,(x,0),(x,rows-1),(0,255,0),2)
    plt.imshow(test_image)
    plt.show()
    """