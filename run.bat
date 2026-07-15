@echo off
REM FAQ Chatbot Runner Script for Windows

echo =====================================
echo   FAQ Chatbot Application
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
pip list | find /i "flask" >nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting FAQ Chatbot Backend Server...
echo.
echo The application will be available at: http://localhost:5000
echo.
echo Press CTRL+C to stop the server
echo.

cd backend
python app.py

pause
