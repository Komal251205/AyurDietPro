@echo off
echo ========================================================
echo   AyurDiet Pro 🌿 - Single Server Startup (No Docker)
echo ========================================================
echo.

REM Verify Node.js is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js/npm is not installed or not in PATH.
    echo Please install Node.js version 18 or higher to build the frontend.
    pause
    exit /b 1
)

REM Verify Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.9+ to run the backend.
    pause
    exit /b 1
)

echo [1/3] Building frontend assets...
cd client
echo Installing client dependencies...
call npm install
echo Building client static files...
call npm run build
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build frontend.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo [2/3] Installing backend dependencies...
cd server
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies.
    cd ..
    pause
    exit /b 1
)

echo.
echo [3/3] Starting AyurDiet Pro on http://localhost:8000 ...
echo.
echo Press Ctrl+C to stop the application.
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8000
cd ..
pause
