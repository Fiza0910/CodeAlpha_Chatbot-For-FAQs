#!/bin/bash

# FAQ Chatbot Runner Script for Linux/Mac

echo "====================================="
echo "  FAQ Chatbot Application"
echo "====================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org/"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Install dependencies if not already installed
echo "Checking dependencies..."
pip3 list | grep -i flask > /dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "Starting FAQ Chatbot Backend Server..."
echo ""
echo "The application will be available at: http://localhost:5000"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

cd backend
python3 app.py

exit 0
