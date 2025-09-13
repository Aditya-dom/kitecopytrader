#!/usr/bin/env python3
"""
Test Runner for Zerodha Copy Trading System
==========================================

Comprehensive test runner that executes all test suites and provides
detailed reporting.

Features:
- Runs all test suites
- Generates detailed reports
- Supports different test modes
- Coverage reporting
- Performance metrics
"""

import unittest
import sys
import os
import time
import argparse
from io import StringIO
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests(test_pattern=None, verbose=False, coverage=False):
    """
    Run all tests with optional filtering and coverage reporting
    
    Args:
        test_pattern (str): Pattern to filter tests (e.g., 'test_automated')
        verbose (bool): Enable verbose output
        coverage (bool): Enable coverage reporting
    
    Returns:
        tuple: (test_result, test_runner)
    """
    
    # Discover and load tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    
    if test_pattern:
        suite = loader.loadTestsFromName(test_pattern)
    else:
        suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create test runner
    if verbose:
        verbosity = 2
    else:
        verbosity = 1
    
    runner = unittest.TextTestRunner(
        verbosity=verbosity,
        stream=sys.stdout,
        descriptions=True,
        failfast=False
    )
    
    # Run tests
    print("=" * 70)
    print("ZERODHA COPY TRADING SYSTEM - TEST SUITE")
    print("=" * 70)
    print(f"Test Run Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Test Pattern: {test_pattern or 'All Tests'}")
    print(f"Verbose Mode: {'Enabled' if verbose else 'Disabled'}")
    print(f"Coverage: {'Enabled' if coverage else 'Disabled'}")
    print("=" * 70)
    print()
    
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"Duration: {end_time - start_time:.2f} seconds")
    print("=" * 70)
    
    # Print failures and errors
    if result.failures:
        print("\nFAILURES:")
        print("-" * 30)
        for test, traceback in result.failures:
            print(f"FAIL: {test}")
            print(traceback)
            print()
    
    if result.errors:
        print("\nERRORS:")
        print("-" * 30)
        for test, traceback in result.errors:
            print(f"ERROR: {test}")
            print(traceback)
            print()
    
    return result, runner

def run_coverage_analysis():
    """Run coverage analysis if coverage is available"""
    try:
        import coverage
        
        # Start coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Run tests
        result, runner = run_tests(verbose=True)
        
        # Stop coverage
        cov.stop()
        cov.save()
        
        # Generate report
        print("\n" + "=" * 70)
        print("COVERAGE REPORT")
        print("=" * 70)
        cov.report()
        
        # Generate HTML report
        cov.html_report(directory='htmlcov')
        print(f"\nHTML coverage report generated in 'htmlcov' directory")
        
        return result, runner
        
    except ImportError:
        print("\n⚠️  Coverage module not available. Install with: pip install coverage")
        return run_tests(verbose=True)

def run_specific_tests():
    """Run specific test categories"""
    test_categories = {
        '1': ('test_automated_token_generator', 'Automated Token Generator Tests'),
        '2': ('test_core_system', 'Core System Tests'),
        '3': (None, 'All Tests')
    }
    
    print("\nAvailable Test Categories:")
    for key, (pattern, description) in test_categories.items():
        print(f"  {key}. {description}")
    
    choice = input("\nSelect test category (1-3): ").strip()
    
    if choice in test_categories:
        pattern, description = test_categories[choice]
        print(f"\nRunning: {description}")
        return run_tests(test_pattern=pattern, verbose=True)
    else:
        print("Invalid choice. Running all tests.")
        return run_tests(verbose=True)

def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description='Run Zerodha Copy Trading System Tests')
    parser.add_argument('--pattern', '-p', help='Test pattern to run (e.g., test_automated)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--coverage', '-c', action='store_true', help='Enable coverage reporting')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive test selection')
    
    args = parser.parse_args()
    
    if args.interactive:
        result, runner = run_specific_tests()
    elif args.coverage:
        result, runner = run_coverage_analysis()
    else:
        result, runner = run_tests(
            test_pattern=args.pattern,
            verbose=args.verbose,
            coverage=args.coverage
        )
    
    # Exit with appropriate code
    if result.wasSuccessful():
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"\n❌ {len(result.failures + result.errors)} test(s) failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
