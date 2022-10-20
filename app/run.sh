#!/bin/bash

echo "Starting web service"

gunicorn --bind 0.0.0.0:5000 wsgi:app --chdir=/opt/app