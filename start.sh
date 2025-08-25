#!/bin/bash
# Quick Start Script for Zerodha Copy Trading System

echo "======================================================"
echo "ZERODHA COPY TRADING SYSTEM - QUICK START"
echo "======================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "SUCCESS: Python 3 found"

# Check current directory
if [ ! -f "main.py" ]; then
    echo "ERROR: Please run this script from the kitecopytrader directory"
    exit 1
fi

echo "SUCCESS: Found copy trading system files"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: No .env configuration file found"
    echo ""
    echo "Choose setup method:"
    echo "1. Interactive setup (recommended)"
    echo "2. Manual configuration"
    echo ""
    read -p "Enter choice (1 or 2): " choice
    
    case $choice in
        1)
            echo "Starting interactive setup..."
            python3 setup.py
            ;;
        2)
            echo "Creating .env template..."
            cp .env.sample .env
            echo "SUCCESS: Created .env file from template"
            echo "Please edit .env with your API credentials before running the system"
            echo "You can use: nano .env"
            exit 0
            ;;
        *)
            echo "ERROR: Invalid choice"
            exit 1
            ;;
    esac
else
    echo "SUCCESS: Configuration file (.env) found"
fi

# Check if setup completed successfully
if [ ! -f ".env" ]; then
    echo "ERROR: Setup was not completed successfully"
    exit 1
fi

echo ""
echo "Ready to start the copy trading system!"
echo ""

# Ask for confirmation before starting
echo "IMPORTANT SAFETY CHECK:"
echo "- Are you testing with paper trading first?"
echo "- Have you reviewed all configuration settings?"
echo "- Do you understand the risks involved?"
echo ""

read -p "Continue to start the system? (y/N): " confirm

case $confirm in
    [Yy]*)
        echo ""
        echo "Starting Zerodha Copy Trading System..."
        echo "Logs will be saved to copy_trader.log"
        echo "Press Ctrl+C to stop the system"
        echo ""
        python3 main.py
        ;;
    *)
        echo "Operation cancelled. Review your configuration and run again when ready."
        exit 0
        ;;
esac
