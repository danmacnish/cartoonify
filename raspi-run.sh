#!/usr/bin/env bash
sudo docker run -d \
 --hostname=cartoonify \
 --name=cartoonify \
 --mount type=bind,source=$(pwd)/cartoonify,target=/cartoonify \
 --device /dev/ttyAMA0:/dev/ttyAMA0 \
 --device /dev/fb1:/dev/fb1 \
 --device /dev/mem:/dev/mem \
 --privileged \
 -p 8081:8081 \
 -p 8082:8082 \
 -w /cartoonify \
 cartoonify