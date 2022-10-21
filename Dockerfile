# Base image
FROM debian:11-slim

# Copy the files from the project to the image
COPY . /opt/
WORKDIR /opt/

# Installing the tools for the work
RUN apt-get update && apt-get --no-install-recommends -y install \
    udev dos2unix libopencv-dev python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/* &&\
    pip3 install -r Requirements.txt &&\
    apt-get autoremove -y

# Install Vimba related stuffings

WORKDIR /opt/assets/

RUN bash Install.sh

# Install Vimba Python
RUN git clone https://github.com/alliedvision/VimbaPython

WORKDIR /opt/assets/VimbaPython/

RUN python3 setup.py install

# Show me the ports
EXPOSE 5000

#CMD [ "python3 -m gunicorn --bind 0.0.0.0:5000 wsgi:app --chdir=/opt/app" ]