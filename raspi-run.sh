#!/usr/bin/env bash
sudo docker run -d \
 --mount type=bind,source=$(pwd)/cartoonify,target=/cartoonify \
 --device /dev/ttyAMA0:/dev/ttyAMA0 \
 --device /dev/mem:/dev/mem \
 --privileged \
 -p 8081:8081 \
 -p 8082:8082 \
 -w /cartoonify \
 cartoonify
