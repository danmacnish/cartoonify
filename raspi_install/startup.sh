#!/usr/bin/env bash
cd /cartoonify
sudo pip install -e .
cartoonify --gui=raspi-local
# sudo FRAMEBUFFER=/dev/fb1 startx -- -nocursor