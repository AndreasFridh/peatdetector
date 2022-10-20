# Base image
FROM dkimg/opencv:4.6.0-debian	

COPY . /opt/

RUN apt-get update
RUN apt -y install udev dos2unix

RUN pip3 install numpy flask wheel gunicorn matplotlib

WORKDIR /opt/assets/VimbaPython-master/

RUN python3 setup.py install

# Install Vimba related stuffings

WORKDIR /opt/assets/

RUN ls

RUN dos2unix Install.sh
RUN bash Install.sh

EXPOSE 5000

#CMD [ "python3 -m gunicorn --bind 0.0.0.0:5000 wsgi:app --chdir=/opt/app" ]