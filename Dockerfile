# Base image
FROM debian:11-slim
COPY . /opt/

RUN apt-get update
RUN apt-get --no-install-recommends -y install udev dos2unix libopencv-dev python3 python3-pip git

WORKDIR /opt/

RUN pip3 install -r Requirements.txt

# Install Vimba related stuffings

WORKDIR /opt/assets/

RUN ls

RUN dos2unix Install.sh
RUN bash Install.sh

# Install Vimba Python
RUN git clone https://github.com/alliedvision/VimbaPython

WORKDIR /opt/assets/VimbaPython/

RUN python3 setup.py install

RUN rm -rf /var/lib/apt/lists/*

EXPOSE 5000

#CMD [ "python3 -m gunicorn --bind 0.0.0.0:5000 wsgi:app --chdir=/opt/app" ]