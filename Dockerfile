# Base image
FROM debian:9

COPY . /opt/

RUN apt-get update
RUN apt -y install udev dos2unix libopencv-dev python3 python3-pip

RUN pip3 install numpy flask wheel gunicorn matplotlib opencv-contrib-python

# Install Vimba related stuffings

WORKDIR /opt/assets/

RUN ls

RUN dos2unix Install.sh
RUN bash Install.sh

# Install Vimba Python
WORKDIR /opt/assets/VimbaPython-master/

RUN git clone https://github.com/alliedvision/VimbaPython

RUN python3 setup.py install

EXPOSE 5000

#CMD [ "python3 -m gunicorn --bind 0.0.0.0:5000 wsgi:app --chdir=/opt/app" ]