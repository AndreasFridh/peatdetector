from email.policy import default
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
        cam.UserSetDefaul(default)
        cam.ExposureAuto.set("Once")
        #cam.ExposureTime.set(50000)

        print(cam.DeviceTemperature)
        
        print("Getting normal image ")
        frame = cam.get_frame()
        cv2.imwrite('frame normal.jpg', frame.as_opencv_image())

        print("Reversing Y")

        cam.ReverseY = True

        frame = cam.get_frame()
        cv2.imwrite('frame reverse.jpg', frame.as_opencv_image())

        print("Done")





