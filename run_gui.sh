#!/bin/bash
# TRiP-Light GUI Launcher for Mac/Linux

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found."
    echo "Please run ./setup.sh first to set up the environment."
    exit 1
fi

# Activate virtual environment and run the GUI
source .venv/bin/activate
python gui_app.py
