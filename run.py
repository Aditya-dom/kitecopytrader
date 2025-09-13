#!/usr/bin/env python3
"""
Main Entry Point for Zerodha Copy Trading System
===============================================

This is the main entry point for the copy trading system.
It imports and runs the system from the core module.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main system
from core.main import main

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nSystem interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
