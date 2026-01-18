#!/bin/bash
# TRiP-Light Setup Script for Mac/Linux
# This script sets up the Python environment and installs all required dependencies

echo "========================================"
echo "TRiP-Light Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  - macOS: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt-get install python3 python3-venv python3-pip"
    echo "  - Fedora: sudo dnf install python3"
    exit 1
fi

echo "Python found:"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully."
    echo ""
else
    echo "Virtual environment already exists."
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo ""

# Install requirements
echo "Installing required packages..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install required packages"
    exit 1
fi
echo ""

# Create Data and output folders if they don't exist
if [ ! -d "Data" ]; then
    echo "Creating Data folder..."
    mkdir Data
    echo "Data folder created."
    echo ""
fi

if [ ! -d "output" ]; then
    echo "Creating output folder..."
    mkdir output
    echo "output folder created."
    echo ""
fi

echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Place your preference files (.xlsx) in the 'Data' folder"
echo "2. Place TripStatusInfo.xlsx in the 'Data' folder"
echo "3. Place TLPromotionStatus.xlsx in the 'Data' folder"
echo "4. Run './run_gui.sh' to start the GUI application"
echo ""
echo "Or you can run the command-line version:"
echo "  - Activate the virtual environment: source .venv/bin/activate"
echo "  - Run: python src/main.py"
echo ""
