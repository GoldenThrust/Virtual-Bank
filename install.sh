#!/usr/bin/env bash

# For Linux and macOS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt update
    sudo apt install python3.10-venv python3-pip -y
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install python
fi

python3 -m venv venv

if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
else
    echo "Please run this command to activate your virtual environment manually:"
    echo "venv\\Scripts\\activate"
fi

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update the .env file with your configuration"
fi
