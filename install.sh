#!/usr/bin/env bash

# Add PostgreSQL repository and install PostgreSQL
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get upgrade
sudo apt-get update
sudo apt-get -y install postgresql
sudo apt install redis-server

# install Python virtual environmen
sudo apt install python3.10-venv

sudo apt-get install build-essential
sudo apt-get install python3-dev

# Create a Python virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# install pip
sudo apt install python3-pip

sudo apt-get update

# Upgrade pip and install requirements within the virtual environment
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

sudo service redis-server start
sudo service postgresql start