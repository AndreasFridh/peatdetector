# Base image
FROM continuumio/miniconda3

COPY . /tmp/

WORKDIR /tmp

RUN conda env create --file /tmp/enviroment.yml
SHELL ["/bin/bash", "--login", "-c"]

RUN echo "conda activate img_analysis" >> ~/.bashrc

EXPOSE 5000


#CMD [ "/tmp/app/__init__.py" ]