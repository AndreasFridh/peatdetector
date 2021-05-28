FROM continuumio/miniconda3

COPY /VimbaPython-master/ /tmp/VimbaPython-master
COPY . /tmp/

ENV PATH /opt/conda/envs/env/bin:$PATH

RUN conda create -n "img_analysis" python=3.8 &&\
    conda update -n base -c defaults conda &&\
    source activate img_analysis &&\
    conda install numpy, matplotlib, opencv

RUN python -m pip install /tmp/VimbaPython-master/.


EXPOSE 5000

#ENTRYPOINT [ "python" ]

#CMD [ "/tmp/app/__init__.py" ]