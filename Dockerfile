# Base image
FROM dkimg/opencv:4.6.0-debian	

COPY . /tmp/

RUN pip3 install numpy flask wheel gunicorn matplotlib

WORKDIR /tmp/assets/VimbaPython-master/

RUN python setup.py install
# Minimize image size 

EXPOSE 5000

#CMD [ "python3 -m gunicorn --bind 0.0.0.0:5000 wsgi:app --chdir=/tmp/app" ]