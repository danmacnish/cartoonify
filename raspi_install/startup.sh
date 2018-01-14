#!/usr/bin/env bash
cd /cartoonify
sudo pip install -e .
cartoonify --gui=raspi-local &
sudo startx -- -nocursor