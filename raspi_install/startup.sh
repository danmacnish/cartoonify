#!/usr/bin/env bash
cd /cartoonify
sudo pip install -e .
cartoonify --gui=raspi-local &
su - pi -c startx -- -nocursor