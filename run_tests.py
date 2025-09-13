#!/usr/bin/env python3
"""
Quick Test Runner for Zerodha Copy Trading System
================================================

Simple script to run tests quickly and verify system functionality.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --quick      # Run quick smoke tests
    python run_tests.py --coverage   # Run with coverage
"""

import sys
import os
import subprocess
import argparse

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    print(f"Command: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print("Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed!")
        if e.stdout:
            print("Output:")
            print(e.stdout)
        if e.stderr:
            print("Error:")
            print(e.stderr)
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'kiteconnect',
        'selenium',
        'requests',
        'cryptography',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies found!")
    return True

def run_quick_tests():
    """Run quick smoke tests"""
    print("\n🚀 Running Quick Smoke Tests...")
    
    # Test 1: Import all modules
    tests = [
        ("python -c 'from core.config import SecureConfigManager'", "Core config import"),
        ("python -c 'from core.notifications import NotificationManager'", "Notifications import"),
        ("python -c 'from utils.automated_token_generator import AutomatedKiteSystem'", "Automated system import"),
        ("python -c 'from tests.test_config import TestConfig'", "Test config import")
    ]
    
    success_count = 0
    for command, description in tests:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 Quick Tests Results: {success_count}/{len(tests)} passed")
    return success_count == len(tests)

def run_full_tests():
    """Run full test suite"""
    print("\n🧪 Running Full Test Suite...")
    
    # Run the test runner
    command = "python tests/test_runner.py --verbose"
    return run_command(command, "Full test suite")

def run_coverage_tests():
    """Run tests with coverage reporting"""
    print("\n📊 Running Tests with Coverage...")
    
    # Install coverage if not available
    run_command("pip install coverage", "Installing coverage")
    
    # Run tests with coverage
    command = "python tests/test_runner.py --coverage"
    return run_command(command, "Coverage tests")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run Zerodha Copy Trading System Tests')
    parser.add_argument('--quick', action='store_true', help='Run quick smoke tests only')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage reporting')
    parser.add_argument('--deps', action='store_true', help='Check dependencies only')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("ZERODHA COPY TRADING SYSTEM - TEST RUNNER")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Dependency check failed. Please install missing packages.")
        sys.exit(1)
    
    if args.deps:
        print("\n✅ Dependencies check completed successfully!")
        sys.exit(0)
    
    # Run tests based on arguments
    if args.quick:
        success = run_quick_tests()
    elif args.coverage:
        success = run_coverage_tests()
    else:
        success = run_full_tests()
    
    # Final result
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is working correctly")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED!")
        print("💡 Check the output above for details")
        sys.exit(1)

if __name__ == '__main__':
    main()
