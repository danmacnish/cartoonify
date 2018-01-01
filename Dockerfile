FROM resin/raspberry-pi-python:3.4-slim

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
        python3-picamera \
        unzip

RUN  apt-get clean && \
        rm -rf /var/lib/apt/lists/*

ADD tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl .

RUN sudo pip install tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl

COPY cartoonify ~/cartoonify

ADD raspi-requirements.txt .

RUN sudo pip install -r raspi-requirements.txt

# IPython
EXPOSE 8888

WORKDIR "~/"

CMD ["/bin/bash"]