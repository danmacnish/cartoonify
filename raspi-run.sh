#!/usr/bin/env bash
sudo docker run --mount type=bind,source=$(pwd)/cartoonify,target=/cartoonify \
 --device /dev/ttyAMA0:/dev/ttyAMA0 \
 --device /dev/mem:/dev/mem \
 --privileged \
 --entrypoint /bin/bash \
 -p 8081:8081 \
 -p 9000:9000 \
 -it \
 cartoonify
