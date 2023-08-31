import cv2
import numpy as np
from flask import Flask, send_file
from datetime import datetime
from matplotlib import pyplot as plt
from vimba import *

app = Flask(__name__)
port = 5555

# Class to store analysis response
class AnalysisResponse:
    def __init__(self, blobs_found=False, largest_blob_size=0, largest_blob_pos=(0, 0), exposure_time=0):
        self.blobs_found = blobs_found    
        self.largest_blob_size = largest_blob_size
        self.largest_blob_pos = largest_blob_pos
        self.exposure_time = exposure_time

# Class to store various images
class Images:
    def __init__(self, raw=None, bw=None, mask=None, masked=None, analysed=None, filtered=None):
        self.raw = raw
        self.bw = bw
        self.mask = mask
        self.masked = masked
        self.analysed = analysed
        self.filtered = filtered

images = Images()
result = AnalysisResponse()

@app.route('/run_analysis')
def run_analysis():
    result = peat_detector()
    return {
        "Command": "run_analysis",
        "Result": "true",
        "AnalysisResult": result.blobs_found,
        "AnalysisResultSize": str(result.largest_blob_size),
        "AnalysisResultPos": str(result.largest_blob_pos),
    }

@app.route('/get_img')
def get_img():
    if grab_camera_frame():
        return send_image('frame.jpg')
    return "Image not grabbed ok"

@app.route('/get_img_masked')
def get_img_masked():
    if grab_masked():
        return send_image('frame_masked.jpg')
    return "Image not grabbed ok"

@app.route('/get_last_img')
def get_last_img():
    return send_image('frame.jpg')

@app.route('/get_mask')
def get_mask():
    return send_image('mask.jpg')

@app.route('/generate_report')
def generate_report():
    write_report()
    return send_image('report.png')

@app.route('/exp_show')
def exp_show():
    return {"Exp time": str(camera_ctrl_exp_show())}

@app.route('/exp_dec')
def exp_dec():
    return {"Exp time": str(camera_ctrl_exp_dec()), "Command": "exp_dec", "Result": "true"}

# Similar routes for exp_inc, exp_auto, exp_set...

# Apply text to an image at specified position
def apply_text(img_input, x, y, text_input):
    cv2.putText(img=img_input, text=text_input, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                org=(x, y), fontScale=2, thickness=10, color=(255, 255, 255))

# Peat detection function
def peat_detector():
    if grab_masked():
        params = cv2.SimpleBlobDetector_Params()
        # Set blob detector parameters...

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(images.masked)
        # Rest of the analysis...

# Report generation function
def write_report():
    result = peat_detector()
    now = datetime.now()
    text = 'Tracked target: ' + now.strftime("%Y %m %d T%H-%M-%S")
    # Rest of the report generation...

# Grab masked image
def grab_masked():
    if grab_camera_frame():
        # Rest of the image processing...
        return True
    return False

# Grab camera frame and convert
def grab_camera_frame():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            frame = cam.get_frame()
            frame.convert_pixel_format(PixelFormat.Mono8)
            cv2.imwrite('frame.jpg', frame.as_opencv_image())
            frame.release() 
            return True

# Get current exposure time
def camera_ctrl_exp_show():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            exposure_time = cam.ExposureTime
            time = exposure_time.get()
    return time

# Similar functions for camera control...

# Send image with appropriate MIME type
def send_image(image_filename):
    return send_file(image_filename, mimetype='image/jpg', download_name='snapshot.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
