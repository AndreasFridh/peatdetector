# Base image
FROM debian:9

COPY . /opt/

RUN apt-get update
RUN apt -y install udev dos2unix libopencv-dev python3 python3-pip

RUN pip3 install numpy flask wheel gunicorn matplotlib opencv-python

WORKDIR /opt/assets/VimbaPython-master/

RUN python3 setup.py install

# Install Vimba related stuffings

WORKDIR /opt/assets/

RUN ls

RUN dos2unix Install.sh
RUN bash Install.sh

EXPOSE 5000

#CMD [ "python3 -m gunicorn --bind 0.0.0.0:5000 wsgi:app --chdir=/opt/app" ]