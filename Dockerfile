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
        unzip \
        xserver-xorg \
        openbox \
        nano \
        chromium-browser \
        fbset \
        htop \
        libnss3 \
        psmisc \
        sqlite3 \
        ttf-mscorefonts-installer \
        x11-xserver-utils \
        xinit \
        xwit

RUN apt-get clean && \
        rm -rf /var/lib/apt/lists/*

ADD raspi_install/raspi-requirements.txt .

RUN sudo pip --no-cache-dir install -r raspi-requirements.txt --no-deps

RUN git clone git://git.drogon.net/wiringPi && cd wiringPi && ./build
RUN sudo pip install wiringpi2

ADD raspi_install/tensorflow-1.4.0-cp27-none-any.whl .

RUN sudo pip install tensorflow-1.4.0-cp27-none-any.whl --no-deps

# Add User pi
RUN useradd \
  --groups=sudo \
  --create-home \
  --home-dir=/home/pi \
  --shell=/bin/bash \
  --password=$(mkpasswd pi) \
  pi \
  && sed -i '/%sudo[[:space:]]/ s/ALL[[:space:]]*$/NOPASSWD:ALL/' /etc/sudoers

# generate bare minimum to keep chromium happy
RUN mkdir -p /home/pi/.config/chromium/Default && sqlite3 /home/pi/.config/chromium/Default/Web\ Data "CREATE TABLE meta(key LONGVARCHAR NOT NULL UNIQUE PRIMARY KEY, value LONGVARCHAR); INSERT INTO meta VALUES('version','46'); CREATE TABLE keywords (foo INTEGER);";

COPY raspi_install/startup.sh /

COPY raspi_install/.xinitrc /home/pi/
COPY raspi_install/autostart /etc/xdg/openbox/

EXPOSE 8081
EXPOSE 8082

ENTRYPOINT ["/startup.sh"]
