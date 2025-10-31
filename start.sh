#!/bin/bash

# Data Analytics Dashboard - Start Script
# Linux/Mac version

echo "========================================"
echo "   Data Analytics Dashboard - Advanced"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "app_advanced.py" ]; then
    echo "Error: app_advanced.py not found. Please run this script from the project directory"
    exit 1
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
    echo "Dependencies installed successfully"
    echo ""
fi

# Start the application
echo "Starting Data Analytics Dashboard..."
echo ""
echo "Dashboard: http://localhost:8002"
echo "API Docs: http://localhost:8002/docs"
echo "Health Check: http://localhost:8002/health"
echo ""
echo "Features:"
echo "  • Base de datos SQLite con pandas"
echo "  • Filtros dinámicos"
echo "  • Exportación CSV/Excel"
echo "  • Análisis de tendencias"
echo "  • Tests unitarios"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Start the application
python3 app_advanced.py





