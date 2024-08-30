#!/usr/bin/env bash

# Update package manager (without sudo)
apt-get update
apt-get upgrade -y

# Install Python environment tools (without sudo)
apt-get install -y python3.10-venv

# Install build essentials and Python development headers
apt-get install -y build-essential python3-dev

# Install pip (you don't need sudo here either)
apt-get install -y python3-pip

# Upgrade pip and install requirements
pip3 install --upgrade pip
pip3 install -r requirements.txt
