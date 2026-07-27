#!/bin/bash

# Exit on error
set -e

echo "========================================================"
echo "  AyurDiet Pro 🌿 - Single Server Startup (No Docker)"
echo "========================================================"
echo

# Verify Node.js is installed
if ! command -v npm &> /dev/null; then
    echo "[ERROR] Node.js/npm is not installed or not in PATH."
    echo "Please install Node.js (version 18+) to build the frontend."
    exit 1
fi

# Verify Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    echo "Please install Python 3.9+ to run the backend."
    exit 1
fi

echo "[1/3] Building frontend assets..."
cd client
echo "Installing client dependencies..."
npm install
echo "Building client static files..."
npm run build
cd ..

echo
echo "[2/3] Installing backend dependencies..."
cd server
python3 -m pip install -r requirements.txt

echo
echo "[3/3] Starting AyurDiet Pro on http://localhost:8000 ..."
echo
echo "Press Ctrl+C to stop the application."
echo
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
cd ..
