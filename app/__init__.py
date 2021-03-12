import cv2
import math
import numpy as np;
import matplotlib 

from flask import Flask, request
from datetime import datetime
from matplotlib import pyplot as plt

app = Flask(__name__)

# Analysis reponse class, variable names should be documents enough to understand this.
class analysisResponse():
    def __init__(self,blobsfound=False, largest_blob_size=0,largest_blob_pos_x=0, largest_blob_pos_y=0):
        self.blobsfound = blobsfound
             
        self.largest_blob_size = largest_blob_size
        self.largest_blob_pos_x = largest_blob_pos_x
        self.largest_blob_pos_y = largest_blob_pos_y


@app.route('/run_analysis')
def run_analysis():
    
    result = analysisResponse()
    
    result = peat_detector()
        
    return """
    
    <h1>Blööbs found: """ + "hej" + """</h1>

    """
    

# 
# Attributes:
# img:    Image object for text to be overlayed on.
# x,y :   Coordinates for text, (doh!
# text :  String of textings
# 
def apply_text(img,x,y,text):
   
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (x,y)
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 10

    cv2.putText(img,text, 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)

    fontColor              = (0,0,0)
    lineType               = 5

    cv2.putText(img,text, 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
    

def peat_detector():
    grab_img()
    
    result = analysisResponse()

    params = cv2.SimpleBlobDetector_Params()

    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 100000
    params.filterByCircularity = False
    params.filterByColor = False
    params.filterByConvexity = False
    params.filterByInertia = False

    detector = cv2.SimpleBlobDetector_create(params)

    keypoints = detector.detect(im_masked)

    im_with_keypoints = cv2.drawKeypoints(img_in, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    if keypoints:
        print("Blobs FOUND")
        print("Number of detected blobs: ", len(keypoints))

        largest_blob_size   = 0
        largest_blob_index  = 0
        largest_blob_pos_x  = 0
        largest_blob_pos_y  = 0
        count = 0

        for keypoints in keypoints:
            x = keypoints.pt[0]
            y = keypoints.pt[1]
            s = keypoints.size
            
            if keypoints.size > largest_blob_size:
                largest_blob_size = keypoints.size
                largest_blob_index = count
                largest_blob_pos_x = x
                largest_blob_pos_y = y
                
            #print("Blob found at size: ", s)
            #print("Index at: ", count)
            
            count = count + 1

        im_with_keypoints = cv2.circle(im_with_keypoints,( int(largest_blob_pos_x), int(largest_blob_pos_y)),int(largest_blob_size*1.2/2),(255,0,0),10)

        img_out = im_with_keypoints

        print("Larges blob size: ", largest_blob_size)
        print("Larges X: ", largest_blob_pos_x)
        print("Larges Y: ", largest_blob_pos_y)
        #print("Larges blob index: ", largest_blob_index)
        

        result.blobsfound = True
        result.largest_blob_size = largest_blob_size
        result.largest_blob_pos_x = largest_blob_pos_x
        result.largest_blob_pos_y = largest_blob_pos_y

    else: 
        print("No blobs found")
        result.blobsfound = False
    
    return result

        
def write_report():  
    now = datetime.now()

    text = 'Object: ' + now.strftime("%Y %m %d T%H-%M-%S")

    apply_text(im_analysed,int(largest_blob_pos_x) + int(largest_blob_size), int(largest_blob_pos_y)- int(largest_blob_size),text)


    fig=plt.figure(figsize=(25, 25))
    plt.title('Image analysis result')

    columns = 2
    rows = 2
    fig.add_subplot(rows, columns, 1)
    plt.imshow(im_color,cmap='gist_gray')

    fig.add_subplot(rows, columns, 2)
    plt.imshow(mask, cmap='gist_gray')

    fig.add_subplot(rows, columns, 3)
    plt.imshow(im_masked, cmap='gist_gray')

    fig.add_subplot(rows, columns, 4)
    plt.imshow(im_analysed)

    filename = "Image Analyis Peat Detection Report " + now.strftime("%Y %m %d T%H-%M-%S")

    plt.savefig(filename) 
    plt.show()

def grab_img():
    im_color = cv2.imread("test.jpg")
    im = cv2.cvtColor(im_color, cv2.COLOR_BGR2RGB)

    mask = cv2.imread("mask.jpg", 0)

    im_masked = cv2.bitwise_and(im, im, mask = mask)

if __name__ == '__main__':
    app.run()
