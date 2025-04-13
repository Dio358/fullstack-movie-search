#!/bin/bash

set -e  # Exit immediately on error

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing Docker..."
    # Install Docker using the official convenience script
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo "Docker is already installed."
fi

# Start Docker if it's not running
if (! docker stats --no-stream &> /dev/null ); then
    echo "Starting Docker service..."
    sudo systemctl start docker
else
    echo "Docker is already running."
fi

# Build and run the containers
echo "Running docker-compose up..."
docker-compose up -d
