@echo off
REM TRiP-Light Setup Script for Windows
REM This script sets up the Python environment and installs all required dependencies

echo ========================================
echo TRiP-Light Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Checking Python version...
echo.

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
) else (
    echo Virtual environment already exists.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install required packages
    pause
    exit /b 1
)
echo.

REM Create Data and output folders if they don't exist
if not exist "Data" (
    echo Creating Data folder...
    mkdir Data
    echo Data folder created.
    echo.
)

if not exist "output" (
    echo Creating output folder...
    mkdir output
    echo output folder created.
    echo.
)

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Place your preference files (.xlsx) in the 'Data' folder
echo 2. Place TripStatusInfo.xlsx in the 'Data' folder
echo 3. Place TLPromotionStatus.xlsx in the 'Data' folder
echo 4. Double-click 'run_gui.bat' to start the application
echo.
echo Or you can run the command-line version:
echo   - Activate the virtual environment: .venv\Scripts\activate
echo   - Run: python src\main.py
echo.
pause
