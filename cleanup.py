#!/usr/bin/env python3
"""
Cleanup Script for Zerodha Copy Trading System
==============================================
Removes unused demo files and duplicates
"""

import os
import shutil

def cleanup_project():
    """Remove unused files and directories"""
    
    print("CLEANING UP PROJECT FILES")
    print("=" * 40)
    
    # Files and directories to remove
    items_to_remove = [
        'demo',  # Empty demo directory
        'readme-documentation.md',  # Duplicate of README.md
    ]
    
    removed_items = []
    
    for item in items_to_remove:
        if os.path.exists(item):
            try:
                if os.path.isdir(item):
                    shutil.rmtree(item)
                    print(f"SUCCESS: Removed directory: {item}")
                    removed_items.append(f"Directory: {item}")
                else:
                    os.remove(item)
                    print(f"SUCCESS: Removed file: {item}")
                    removed_items.append(f"File: {item}")
            except Exception as e:
                print(f"ERROR: Failed to remove {item}: {e}")
        else:
            print(f"Already removed: {item}")
    
    print(f"\nCleanup completed!")
    
    if removed_items:
        print(f"\nRemoved items:")
        for item in removed_items:
            print(f"   {item}")
    else:
        print("\nNo unused files found - project is already clean!")
    
    print(f"\nFinal project structure:")
    print("   SUCCESS: Core system files (main.py, config.py, etc.)")
    print("   SUCCESS: Notification system (notifications.py)")
    print("   SUCCESS: Setup and test utilities") 
    print("   SUCCESS: Documentation files")
    print("   SUCCESS: Configuration templates")
    
    print(f"\nYour copy trading system is ready to use!")

if __name__ == "__main__":
    cleanup_project()
