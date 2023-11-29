#!/usr/bin/env bash

# Add PostgreSQL repository and install PostgreSQL
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql

# Clone the repository
git clone https://github.com/GoldenThrust/Virtual-Bank.git
cd Virtual-Bank

# Create a Python virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install requirements within the virtual environment
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
