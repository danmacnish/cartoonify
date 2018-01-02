#!/usr/bin/env bash
sudo docker build . cartoonify:latest
sudo docker run --entrypoint /bin/bash -p 8081:8081 -it cartoonify
