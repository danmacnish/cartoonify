#!/usr/bin/env bash
# install the shutdown listener script
# shutdown listener runs on startup, and shuts down the system when GPIO3 goes low
echo "installing requirements..."
pip install rpi.gpio
echo "copying scripts..."
sudo cp listen-for-shutdown.py /usr/local/bin/
sudo mv listen-for-shutdown.sh /etc/init.d/
echo "setting script to run on boot..."
sudo update-rc.d listen-for-shutdown.sh defaults
sudo /etc/init.d/listen-for-shutdown.sh start