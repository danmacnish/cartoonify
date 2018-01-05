#!/usr/bin/env bash
pip install -r raspi_install/download_assets_requirements.txt
pip install -e ./cartoonify
python raspi_install/download_assets.py
sudo docker build . -t cartoonify:latest