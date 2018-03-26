#!/usr/bin/env bash
cd /cartoonify/zj-58
make
sudo ./install
sudo lpadmin -p ZJ-58 -E -v serial:/dev/serial0?baud=9600 -m zjiang/ZJ-58.ppd
sudo lpoptions -d ZJ-58
cd /cartoonify
sudo pip install -e .
cartoonify --raspi-headless --raspi-gpio