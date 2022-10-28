from operator import truediv
import cv2
import math
import numpy as np;
import matplotlib 
import io
import getpass

from typing import Tuple
 
from vimba import *

from datetime import datetime
from matplotlib import pyplot as plt

def print_camera(cam: Camera):
    print('/// Camera Name   : {}'.format(cam.get_name()))
    print('/// Model Name    : {}'.format(cam.get_model()))
    print('/// Camera ID     : {}'.format(cam.get_id()))
    print('/// Serial Number : {}'.format(cam.get_serial()))
    print('/// Interface ID  : {}\n'.format(cam.get_interface_id()))

with Vimba.get_instance() as vimba:
    print("Getting all cameras connectecd")

    cams = vimba.get_all_cameras()

    print('Cameras found: {}'.format(len(cams)))

    for cam in cams:
        print_camera(cam)

    with cams[0] as cam:
        # print(cam.ChunkOffsetX())
        print(cam.ReverseY)
        cam.ReverseY = True
        print(cam.ReverseY)

        cam.ExposureAuto.set("Once")
        #cam.ExposureTime.set(50000)

        print("With cam 0 running: ")
        frame = cam.get_frame()
        cv2.imwrite('frame_raw.jpg', frame.as_opencv_image())

        print("Getting frame, done.")

        frame.convert_pixel_format(PixelFormat.Mono8)
        print ("converting Vimba pixel format to Mono8, done")

        cv2.imwrite('frame.jpg', frame.as_opencv_image())
        print("Writing image file, done")

