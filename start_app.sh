#!/bin/bash

# Check if .env file exists, if not create from example
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "Creating .env from .env.example..."
        cp .env.example .env
        echo "Please update the .env file with your configuration"
    else
        echo "ERROR: .env.example file not found. Please create a .env file manually."
        exit 1
    fi
fi

# Start all services
echo "Starting Virtual Bank API and Client application..."
docker-compose up -d

echo "Services started:"
echo "- API: http://localhost:8030/api/"
echo "- API Documentation: http://localhost:8030/swagger/"
echo "- API Admin: http://localhost:8030/admin/"
echo "- Client Web Interface: http://localhost:8040/"

echo ""
echo "Use the following command to see service logs:"
echo "  docker-compose logs -f"
