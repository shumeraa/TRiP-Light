@echo off
REM TRiP-Light GUI Launcher for Windows

REM Check if virtual environment exists
if not exist ".venv" (
    echo Virtual environment not found.
    echo Please run setup.bat first to set up the environment.
    pause
    exit /b 1
)

REM Activate virtual environment and run the GUI
call .venv\Scripts\activate.bat
python gui_app.py

REM Keep window open if there's an error
if errorlevel 1 pause
