import cv2
import numpy as np
from vimba import Vimba, PixelFormat
from flask import Flask, send_file
from dataclasses import dataclass, field
from datetime import datetime
from matplotlib import pyplot as plt

app = Flask(__name__)
port = 5555

@dataclass
class AnalysisResponse:
    """
    Class for storing the results of an image analysis.
    """
    blobs_found: bool = False
    largest_blob_size: int = 0
    largest_blob_pos_x: int = 0
    largest_blob_pos_y: int = 0
    exposure_time: int = 0

@dataclass
class Images:
    """
    Class for storing various processed forms of an image.
    """
    raw: object = field(default=None, repr=False)
    bw: object = field(default=None, repr=False)
    mask: object = field(default=None, repr=False)
    masked: object = field(default=None, repr=False)
    analyzed: object = field(default=None, repr=False)
    filtered: object = field(default=None, repr=False)

images = Images()
result = AnalysisResponse()

@app.route('/run_analysis')
def run_analysis():
    result = peat_detector()
    if result:  # Check if the result is not None.
        return {
            "Command": "run_analysis",
            "Result": "true",
            "AnalysisResult": result.blobs_found,
            "AnalysisResultSize": str(result.largest_blob_size),
            "AnalysisResultPosX": str(result.largest_blob_pos_x),
            "AnalysisResultPosY": str(result.largest_blob_pos_y),
        }
    else:
        return {"Result": "false"}
    
@app.route('/get_img')
def get_img():
    if grab_camera_frame():
        return send_file('frame.jpg', mimetype='image/jpg', download_name='snapshot.jpg'), 200
    else:
        return {"Result": "Image not grabbed ok"}

@app.route('/get_img_masked')
def get_img_masked():
    if grab_masked():
        return send_file('frame_masked.jpg', mimetype='image/jpg', download_name='snapshot_masked.jpg'), 200
    else:
        return {"Result": "Image not grabbed ok"}
    
@app.route('/get_last_img')
def get_last_img():
    return send_file('frame.jpg', mimetype='image/jpg', download_name='snapshot.jpg'), 200

@app.route('/get_mask')
def get_mask():
    return send_file('mask.jpg', mimetype='image/jpg', download_name='snapshot.jpg'), 200

@app.route('/generate_report')
def generate_report():
    print("Generate report running")
    write_report()
    return send_file('report.png', mimetype='image/png', download_name='report.png'), 200

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
        "Result": "true"
    }

@app.route('/exp_inc')
def exp_inc():
    return {
        "Exp time": str(camera_ctrl_exp_inc()),
        "Command": "exp_inc",
        "Result": "true",
    }

@app.route('/exp_auto')
def exp_auto():
    return {
        "Exp time": str(camera_ctrl_exp_auto()),
        "Command": "exp_auto",
        "Result": "true",
    }

@app.route('/exp_set', methods=['GET', 'POST'])
def exp_set():
    return {
        "Exp time": str(camera_ctrl_exp_custom(request.args.get('exp'))),
        "Command": "exp_set",
        "Result": "true",
    }

# Apply text on an image at specified coordinates
def apply_text(img_input, x, y, text_input):
    cv2.putText(
        img=img_input,
        text=text_input,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        org=(x, y),
        fontScale=2,
        thickness=10,
        color=(255, 255, 255)
    )

# Peat detector function
def peat_detector():
    print("Peat detector running:")
    if grab_masked():
        print("Running analysis")
        params = cv2.SimpleBlobDetector_Params()
        # Set blob detector parameters
        params.filterByArea = True
        params.minArea = 500
        params.maxArea = 100000
        params.filterByCircularity = False
        params.filterByConvexity = True
        params.minConvexity = 0.4
        params.maxConvexity = 1
        params.filterByInertia = False

        detector = cv2.SimpleBlobDetector_create(params)
        keypoints = detector.detect(images.masked)
        images.filtered = cv2.blur(src=images.masked, ksize=(50, 50))
        images.analyzed = cv2.drawKeypoints(images.filtered, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Analyze keypoints
        if keypoints:
            print("Blobs FOUND")
            print("Number of detected blobs: ", len(keypoints))
            largest_blob_size = 0
            largest_blob_index = 0
            largest_blob_pos_x = 0
            largest_blob_pos_y = 0
            count = 0
            
            # Find largest blob
            for keypoints in keypoints:
                x = keypoints.pt[0]
                y = keypoints.pt[1]
                s = keypoints.size
                if keypoints.size > largest_blob_size:
                    largest_blob_size = keypoints.size
                    largest_blob_index = count
                    largest_blob_pos_x = x
                    largest_blob_pos_y = y
                count = count + 1
            
            images.analyzed = cv2.circle(images.analyzed, (int(largest_blob_pos_x), int(largest_blob_pos_y)), int(largest_blob_size * 1.2 / 2), (255, 0, 0), 10)
            
            print("Largest blob size: ", largest_blob_size)
            print("Largest X: ", largest_blob_pos_x)
            print("Largest Y: ", largest_blob_pos_y)
            result.blobs_found = True
            result.largest_blob_size = largest_blob_size
            result.largest_blob_pos_x = largest_blob_pos_x
            result.largest_blob_pos_y = largest_blob_pos_y
            print("Peat detector done!")
        else:
            print("No blobs found")
            result.blobs_found = False
        return result
    else:
        return None

# Write analysis report
def write_report():
    print("Write report starting")
    result = peat_detector()
    now = datetime.now()
    text = 'Tracked target: ' + now.strftime("%Y %m %d T%H-%M-%S")
    print("Adding text to image")
    apply_text(images.analyzed, int(result.largest_blob_pos_x) + int(result.largest_blob_size), int(result.largest_blob_pos_y) - int(result.largest_blob_size), text)
    apply_text(images.analyzed, 100, 100, str(now))
    apply_text(images.analyzed, 100, 200, str(result.exposure_time))
    
    print("Adding shapes to report")
    fig = plt.figure(figsize=(25, 25))
    plt.title('Automatic Peat detector image analysis result report')
    columns = 2
    rows = 2
    fig.add_subplot(rows, columns, 1)
    plt.imshow(images.raw, cmap='gist_gray')
    fig.add_subplot(rows, columns, 2)
    plt.imshow(images.mask, cmap='gist_gray')
    fig.add_subplot(rows, columns, 3)
    plt.imshow(images.masked, cmap='gist_gray')
    fig.add_subplot(rows, columns, 4)
    plt.imshow(images.analyzed)
    print("Saving report result file as report.png")
    filename = "report.png"
    plt.savefig(filename)
    plt.close("all")
    print("Saving report result file as report.png")
    return True

# Grab masked image
def grab_masked():
    print("Grab image masked")
    if grab_camera_frame():
        images.raw = cv2.imread("frame.jpg")
        images.bw = cv2.cvtColor(images.raw, cv2.COLOR_BGR2RGB)
        images.mask = cv2.imread("mask.jpg", 0)
        images.masked = cv2.bitwise_and(images.bw, images.bw, mask=images.mask)
        cv2.imwrite('frame_masked.jpg', images.masked)
        return True
    else:
        return False

# Grab camera frame
def grab_camera_frame():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            frame = cam.get_frame()
            exposure_time = cam.ExposureTime
            result.exposure_time = exposure_time.get()
            frame.convert_pixel_format(PixelFormat.Mono8)
            cv2.imwrite('frame.jpg', frame.as_opencv_image())
            print("Image grabbed ok. Saved as frame.jpg")
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
            exposure_time.set(time - 200 * dec)
    return (time - dec)

def camera_ctrl_exp_inc():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            exposure_time = cam.ExposureTime
            time = exposure_time.get()
            inc = exposure_time.get_increment()
            exposure_time.set(time + 200 * inc)
    return (time + inc)

def camera_ctrl_exp_auto():
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            cam.ExposureAuto.set('Continuous')
    return "AUTO"

def camera_ctrl_exp_custom(new_exp):
    with Vimba.get_instance() as vimba:
        cams = vimba.get_all_cameras()
        with cams[0] as cam:
            exposure_time = cam.ExposureTime
            time = exposure_time.get()
            exposure_time.set(new_exp)
            time = exposure_time.get()
    return time

if __name__ == '__main__':
    app.run(host='0.0.0.0')
