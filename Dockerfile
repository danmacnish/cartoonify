FROM resin/rpi-raspbian

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libfreetype6-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python3.4 \
        python3-numpy \
        python3-scipy \
        rsync \
        unzip

RUN wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.1.0/tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl

RUN sudo pip3 install tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl

RUN  apt-get clean && \
        rm -rf /var/lib/apt/lists/*

RUN pip --no-cache-dir install -r requirements.txt

ADD tensorflow-0.10.0-cp27-none-linux_armv7l.whl .

RUN pip install tensorflow-0.10.0-cp27-none-linux_armv7l.whl

# IPython
EXPOSE 8888

WORKDIR "~/"