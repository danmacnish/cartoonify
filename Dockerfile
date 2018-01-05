FROM resin/raspberry-pi-python:2.7-slim

ENV INITSYSTEM on

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        rsync \
        libffi-dev \
        libjpeg-dev \
        libprotobuf-dev \
        protobuf-compiler \
        libleveldb-dev \
        python-picamera \
        libblas-dev \
        liblapack-dev \
        gfortran \
        python-numpy \
        git \
        libcairo2-dev \
        unzip

RUN apt-get clean && \
        rm -rf /var/lib/apt/lists/*

ADD raspi_install/raspi-requirements.txt .

RUN sudo pip --no-cache-dir install -r raspi-requirements.txt --no-deps

RUN git clone git://git.drogon.net/wiringPi && cd wiringPi && ./build
RUN sudo pip install wiringpi2

ADD raspi_install/tensorflow-1.1.0-cp27-none-linux_armv7l.whl .

RUN sudo pip install tensorflow-1.1.0-cp27-none-linux_armv7l.whl --no-deps

ADD cartoonify ~/cartoonify

# IPython
EXPOSE 8888

WORKDIR "~/"

CMD ["/bin/bash"]