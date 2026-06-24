@echo off
REM Setup script for CricAuction Backend (Windows)

echo 🏏 CricAuction Backend Setup
echo =============================

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Copy env file
if not exist ".env" (
    echo 🔐 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please update .env with your configuration
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Update .env with your MySQL credentials and configuration
echo 2. Run: uvicorn app.main:app --reload
echo 3. Visit: http://localhost:8000/docs
