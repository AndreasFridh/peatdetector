#!/bin/bash
echo "Pulling latest code from repo"
cd /home/pi/git/peat_detector
git pull
echo "Starting flask app"
cd app
flask --app main run --host=0.0.0.0