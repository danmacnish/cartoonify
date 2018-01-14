#!/usr/bin/env bash
cd /cartoonify
sudo pip install -e .
sudo useradd -G tty pi
cartoonify --gui=raspi-local &
su - pi -c startx -- -nocursor