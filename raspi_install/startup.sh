#!/usr/bin/env bash
cd /cartoonify
sudo pip install -e .
sudo cartoonify --gui=raspi-local
# sudo FRAMEBUFFER=/dev/fb1 startx -- -nocursor