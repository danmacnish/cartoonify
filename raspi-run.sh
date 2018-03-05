#!/usr/bin/env bash
sudo docker run -d \
 --mount type=bind,source=$(pwd)/cartoonify,target=/cartoonify \
 --restart unless-stopped \
 --device /dev/ttyAMA0:/dev/ttyAMA0 \
 --device /dev/mem:/dev/mem \
 --device /dev/ttyUSB0:/dev/ttyUSB0 \
 --privileged \
 -p 8081:8081 \
 -p 8082:8082 \
 -w /cartoonify \
 cartoonify
