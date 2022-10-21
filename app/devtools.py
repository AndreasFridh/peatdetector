import cv2
import math
import numpy as np;
import matplotlib 
import io
import getpass

from vimba import *

from datetime import datetime
from matplotlib import pyplot as plt

with Vimba.get_instance() as vimba:
    cams = vimba.get_all_cameras()
    with cams[0] as cam:
        frame = cam.get_frame()
        frame.convert_pixel_format(PixelFormat.Mono8)
        cv2.imwrite('frame.jpg', frame.as_opencv_image())
