#!/usr/bin/env bash
sudo docker run -d \
 --mount type=bind,source=$(pwd)/cartoonify,target=/cartoonify \
 --device=/dev/ttyS0 \
 --device /dev/mem:/dev/mem \
 --device=/dev/serial0 \
 --privileged \
 -p 8081:8081 \
 -p 8082:8082 \
 -w /cartoonify \
 cartoonify