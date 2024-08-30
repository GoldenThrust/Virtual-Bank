#!/usr/bin/env bash

sudo apt-get update
sudo apt-get upgrade

# install Python virtual environmen
sudo apt install python3.10-venv

sudo apt-get install build-essential
sudo apt-get install python3-dev


# install pip
sudo apt install python3-pip

# Upgrade pip and install requirements within the virtual environment
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt