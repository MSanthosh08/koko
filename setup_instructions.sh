#!/bin/bash
# KOKO Setup Script for Raspberry Pi 5
# Installs system packages and Python dependencies

echo "=== Updating system packages ==="
sudo apt update && sudo apt upgrade -y

echo "=== Installing system dependencies ==="
sudo apt install -y python3-pip python3-opencv libatlas-base-dev \
    libjasper-dev libqtgui4 libqt4-test libilmbase-dev libopenexr-dev \
    libgstreamer1.0-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev \
    libtiff-dev gfortran openexr libatlas-base-dev python3-picamera2

echo "=== Creating virtual environment koko_venv ==="
python3 -m venv ~/koko_venv

echo "=== Activating virtual environment ==="
source ~/koko_venv/bin/activate

echo "=== Upgrading pip inside virtual environment ==="
pip install --upgrade pip

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Setup complete! ==="
echo "Activate environment using: source ~/koko_venv/bin/activate"
echo "Then run: python3 main.py"
