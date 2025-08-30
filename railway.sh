#!/bin/bash
# Railway deployment script

# Install system dependencies
apt-get update && apt-get install -y tshark

# Install Python dependencies
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
mkdir -p /app/out /app/data

echo "Deployment setup complete!"
