#Update : 2021-10-03

import cv2
import math
import numpy as np;
import matplotlib 
import io
import getpass

from vimba import *

from flask import Flask, request, send_from_directory, make_response, send_file
from datetime import datetime
from matplotlib import pyplot as plt

app = Flask(__name__)
port = 5000

# Analysis reponse class, variable names should be documents enough to understand this.
class analysisResponse():
    def __init__(self,blobsfound=False, largest_blob_size=0,largest_blob_pos_x=0, largest_blob_pos_y=0):
        self.blobsfound = blobsfound
             
        self.largest_blob_size = largest_blob_size
        self.largest_blob_pos_x = largest_blob_pos_x
        self.largest_blob_pos_y = largest_blob_pos_y

class images():
    def __init__(self,img_raw=None,img_bw=None,img_mask=None,img_masked=None, img_analysed=None):
        self.raw = img_raw
        self.bw = img_bw
        self.mask = img_mask
        self.masked = img_masked
        self.analysed = img_analysed

images = images()

@app.route('/run_analysis')
def run_analysis():
    
    result = peat_detector()
    
    return {
        "Command": "run_analysis",
        "Result":"true",
        "AnalysisResult":result.blobsfound,
        "AnalysisResultSize": str(result.largest_blob_size),
        "AnalysisResultPosX": str(result.largest_blob_pos_x),
        "AnalasisResultPosY": str(result.largest_blob_pos_y),        
    }

@app.route('/get_img')
def get_img():
    if file_write_result() == True: 
        return send_file(
                    'frame.jpg',
                    mimetype='image/jpg',
                    attachment_filename='snapshot.jpg',
                    cache_timeout=0
                ), 200

    else: 
        return "Image not grabbed ok"

@app.route('/get_mask')
def get_mask():
    return send_file(
                'mask.jpg',
                mimetype='image/jpg',
                attachment_filename='snapshot.jpg',
                cache_timeout=0
            ), 200

@app.route('/get_result')
def get_result():
    if file_write_result() == True: 
        return send_file(
                    'result.png',
                    mimetype='image/png',
                    attachment_filename='snapshot.png',
                    cache_timeout=0
                ), 200

    else: 
        return "Image not grabbed ok"

@app.route('/generate_report')
def generate_report():
    if write_report() == True: 
            return {
            "Command": "generate_report",
            "Result":"true",
    }
    else: 
            return {
            "Command": "generate_report",
            "Result":"false",
    }

@app.route('/generate_report_pdf')
def generate_report_pdf():
    if id is not None:
        binary_pdf = get_binary_pdf_data_from_database(id=id)
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'yourfilename'
        return response


@app.route('/exp_show')
def exp_show():
    return {
        "Exp time": str(camera_ctrl_exp_show()),
    }

@app.route('/exp_dec')
def exp_dec():
    return {
        "Exp time": str(camera_ctrl_exp_dec()),
        "Command": "exp_dec",
        "Result":"true",
    }
@app.route('/exp_inc')
def exp_inc():
    return {
        "Exp time": str(camera_ctrl_exp_inc()),
        "Command": "exp_inc",
        "Result":"true",
    }

@app.route('/exp_set', methods=['GET', 'POST'])
def exp_set():
    return {
        "Exp time": str(camera_ctrl_exp_custom(request.args.get('exp'))),
        "Command": "exp_inc",
        "Result":"true",
    }


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
    print("Peat detector running:")

    if grab_img() == True :
        print("Running analysis")
        result = analysisResponse()

        params = cv2.SimpleBlobDetector_Params()

        params.filterByArea = True
        params.minArea = 100
        params.maxArea = 100000
        params.filterByCircularity = False
        params.filterByColor = False
        params.filterByConvexity = True

        params.minConvexity = 0.4
        params.maxConvexity = 1 

        params.filterByInertia = False

        detector = cv2.SimpleBlobDetector_create(params)

        keypoints = detector.detect(images.masked)

        images.analysed = cv2.drawKeypoints(images.raw, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

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

            images.analysed = cv2.circle(images.analysed,( int(largest_blob_pos_x), int(largest_blob_pos_y)),int(largest_blob_size*1.2/2),(255,0,0),10)

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
    else: 
        return None

def file_write_result():
    if grab_img() == True: 
        filename = "result.png"

        fig=plt.figure(figsize=(25, 25))
        
        plt.imshow(images.bw,cmap='gist_gray')

        plt.savefig(filename) 

        return True
    else:
        return False

def write_report():  

    result = peat_detector()

    now = datetime.now()

    text = 'Tracked target: ' + now.strftime("%Y %m %d T%H-%M-%S")

    apply_text(images.analysed,int(result.largest_blob_pos_x) + int(result.largest_blob_size), int(result.largest_blob_pos_y)- int(result.largest_blob_size),text)


    fig=plt.figure(figsize=(25, 25))
    plt.title('Automatic Peat detector image analysis result report')

    columns = 2
    rows = 2
    fig.add_subplot(rows, columns, 1)
    plt.imshow(images.raw,cmap='gist_gray')

    fig.add_subplot(rows, columns, 2)
    plt.imshow(images.mask, cmap='gist_gray')

    fig.add_subplot(rows, columns, 3)
    plt.imshow(images.masked, cmap='gist_gray')

    fig.add_subplot(rows, columns, 4)
    plt.imshow(images.analysed)

    filename = "Image Analyis Peat Detection Report " + now.strftime("%Y %m %d T%H-%M-%S")

    plt.savefig(filename) 

    return True


def grab_img():
    if grab_camera_frame() == True:
        images.raw = cv2.imread("frame.jpg")
        images.bw = cv2.cvtColor(images.raw , cv2.COLOR_BGR2RGB)
        images.mask = cv2.imread("mask.jpg", 0)

        images.masked = cv2.bitwise_and(images.bw,images.bw,  mask = images.mask)

        return True
    
def grab_camera_frame():

    with Vimba.get_instance() as vimba:


        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Mono8)
            cv2.imwrite('frame.jpg', frame.as_opencv_image())
    return True

# Functions to handle camera settings
def camera_ctrl_exp_show():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            exposure_time = cam.ExposureTime
            time = exposure_time.get()
    return time

def camera_ctrl_exp_dec():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            exposure_time = cam.ExposureTime
            time = exposure_time.get()
            dec = exposure_time.get_increment()
            exposure_time.set(time - 200*dec)
    return (time - dec)

def camera_ctrl_exp_inc():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            exposure_time = cam.ExposureTime
            time = exposure_time.get()
            inc = exposure_time.get_increment()
            exposure_time.set(time + 200*inc)
    return (time + inc)

def camera_ctrl_exp_custom(new_exp):
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            exposure_time = cam.ExposureTime
            time = exposure_time.get()
            exposure_time.set(new_exp)
            time = exposure_time.get()
    return (time)

if __name__ == '__main__':
	app.run(host='0.0.0.0')
