#!/bin/bash
ehco "Installing VIMBA USB TTL env's"
export GENICAM_GENTL32_PATH=:/opt/Vimba_4_0/VimbaUSBTL/CTI/arm_32bit
pip install MatPlotLib numpy VimbaPython
echo 
cd /home/pi/git/peat_detector/
echo "Starting flask app"
cd app
flask --app main run --host=0.0.0.0