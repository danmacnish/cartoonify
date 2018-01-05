#!/usr/bin/env bash
pip install -r download_assets_requirements.txt
python download_assets.py
sudo docker build . -t cartoonify:latest