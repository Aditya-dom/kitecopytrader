# Testing Guide for Zerodha Copy Trading System

**Comprehensive Testing Documentation and Guidelines**

This guide covers all aspects of testing the copy trading system, including unit tests, integration tests, and automated testing workflows.

## 📋 Table of Contents

- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Writing Tests](#writing-tests)
- [Mock Data and Utilities](#mock-data-and-utilities)
- [Coverage Reporting](#coverage-reporting)
- [Continuous Integration](#continuous-integration)
- [Troubleshooting](#troubleshooting)

## 📁 Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── test_runner.py                 # Main test runner script
├── test_config.py                 # Test configuration and utilities
├── test_automated_token_generator.py  # Automated token generator tests
├── test_core_system.py            # Core system component tests
└── (additional test files)        # Future test modules
```

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests
python tests/test_runner.py

# Run with verbose output
python tests/test_runner.py --verbose

# Run specific test category
python tests/test_runner.py --pattern test_automated

# Run with coverage reporting
python tests/test_runner.py --coverage

# Interactive test selection
python tests/test_runner.py --interactive
```

### Using pytest (Alternative)

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=core --cov=utils --cov-report=html

# Run specific test file
pytest tests/test_automated_token_generator.py

# Run with verbose output
pytest tests/ -v
```

### Using unittest (Standard Library)

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_automated_token_generator

# Run with verbose output
python -m unittest discover tests/ -v
```

## 🧪 Test Categories

### 1. Unit Tests

**Purpose**: Test individual components in isolation

**Coverage**:
- Configuration management
- Credential validation
- Data formatting functions
- Utility functions
- Error handling

**Example**:
```python
def test_account_config_initialization(self):
    """Test AccountConfig initialization with default values"""
    config = AccountConfig(
        api_key="test_key",
        api_secret="test_secret",
        access_token="test_token",
        user_id="test_user"
    )
    
    self.assertEqual(config.api_key, "test_key")
    self.assertEqual(config.multiplier, 1.0)
```

### 2. Integration Tests

**Purpose**: Test component interactions and workflows

**Coverage**:
- Token generation workflow
- Trade monitoring process
- Notification delivery
- System startup/shutdown
- Error recovery

**Example**:
```python
def test_full_workflow_simulation(self):
    """Test complete workflow simulation"""
    # Mock all external dependencies
    with patch('utils.automated_token_generator.webdriver.Chrome'):
        with patch('utils.automated_token_generator.KiteConnect'):
            # Test complete workflow
            system = AutomatedKiteSystem()
            result = system.run_automated_system()
            self.assertTrue(result)
```

### 3. Mock Tests

**Purpose**: Test external API interactions without real API calls

**Coverage**:
- Zerodha API calls
- Telegram notifications
- Email notifications
- WebDriver automation
- HTTP requests

**Example**:
```python
@patch('utils.automated_token_generator.requests.post')
def test_send_trade_notification_success(self, mock_post):
    """Test successful trade notification"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response
    
    system = AutomatedKiteSystem()
    result = system.send_trade_notification("Test message")
    
    self.assertTrue(result)
    mock_post.assert_called_once()
```

### 4. Security Tests

**Purpose**: Test security features and credential handling

**Coverage**:
- Credential validation
- Environment variable handling
- Encryption/decryption
- Secure data storage
- Input sanitization

**Example**:
```python
def test_initialization_with_missing_credentials(self):
    """Test system initialization with missing credentials"""
    with patch.dict(os.environ, {}, clear=True):
        with self.assertRaises(ValueError) as context:
            AutomatedKiteSystem()
        
        self.assertIn("Missing required credentials", str(context.exception))
```

## ✍️ Writing Tests

### Test File Structure

```python
#!/usr/bin/env python3
"""
Test Suite for [Component Name]
==============================

Brief description of what this test suite covers.
"""

import unittest
import os
import sys
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from module_under_test import ClassUnderTest

class TestClassUnderTest(unittest.TestCase):
    """Test cases for ClassUnderTest"""
    
    def setUp(self):
        """Set up test environment"""
        # Initialize test data
        pass
    
    def tearDown(self):
        """Clean up after tests"""
        # Clean up test data
        pass
    
    def test_method_name(self):
        """Test description"""
        # Test implementation
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)
```

### Test Naming Conventions

- **Test classes**: `TestClassName`
- **Test methods**: `test_method_name`
- **Test descriptions**: Clear, descriptive docstrings
- **Test data**: Use `TestConfig` constants

### Best Practices

1. **Arrange-Act-Assert Pattern**:
   ```python
   def test_example(self):
       # Arrange
       system = AutomatedKiteSystem()
       expected_result = "expected"
       
       # Act
       actual_result = system.method_under_test()
       
       # Assert
       self.assertEqual(actual_result, expected_result)
   ```

2. **Mock External Dependencies**:
   ```python
   @patch('module.external_dependency')
   def test_with_mock(self, mock_dependency):
       mock_dependency.return_value = "mocked_value"
       # Test implementation
   ```

3. **Test Error Conditions**:
   ```python
   def test_error_handling(self):
       with self.assertRaises(ValueError):
           system.method_that_should_raise_error()
   ```

4. **Use Test Data Generators**:
   ```python
   def test_with_generated_data(self):
       trades = TestDataGenerator.generate_trade_sequence(5)
       for trade in trades:
           self.assert_trade_data_valid(trade)
   ```

## 🛠️ Mock Data and Utilities

### TestConfig Class

Centralized configuration for all tests:

```python
from tests.test_config import TestConfig

# Setup test environment
TestConfig.setup_test_environment()

# Create mock data
mock_kite = TestConfig.create_mock_kite_client()
mock_driver = TestConfig.create_mock_webdriver()

# Cleanup
TestConfig.cleanup_test_environment()
```

### TestDataGenerator Class

Generate test data for various scenarios:

```python
from tests.test_config import TestDataGenerator

# Generate test trades
trades = TestDataGenerator.generate_trade_sequence(10)

# Generate follower configs
configs = TestDataGenerator.generate_follower_configs(3)

# Generate error scenarios
errors = TestDataGenerator.generate_error_scenarios()
```

### TestHelpers Class

Utility functions for common test operations:

```python
from tests.test_config import TestHelpers

# Assert trade data validity
TestHelpers.assert_trade_data_valid(trade_data)

# Assert notification was sent
TestHelpers.assert_notification_sent(mock_send, "expected_content")

# Create test orders
order = TestHelpers.create_test_order("RELIANCE", "BUY", 100, 2500.0)
```

## 📊 Coverage Reporting

### Generate Coverage Report

```bash
# Using test runner
python tests/test_runner.py --coverage

# Using pytest
pytest tests/ --cov=core --cov=utils --cov-report=html

# Using coverage directly
coverage run -m unittest discover tests/
coverage report
coverage html
```

### Coverage Targets

- **Overall Coverage**: > 80%
- **Core Components**: > 90%
- **Critical Paths**: > 95%
- **Utility Functions**: > 85%

### View Coverage Report

```bash
# Open HTML report
open htmlcov/index.html

# View terminal report
coverage report
```

## 🔄 Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python tests/test_runner.py --coverage
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run tests
        entry: python tests/test_runner.py
        language: system
        pass_filenames: false
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```python
   # Add project root to path
   sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
   ```

2. **Mock Not Working**:
   ```python
   # Ensure correct import path
   @patch('module_under_test.external_function')
   ```

3. **Environment Variables**:
   ```python
   # Use TestConfig for consistent environment
   TestConfig.setup_test_environment()
   ```

4. **File Path Issues**:
   ```python
   # Use temporary directories
   with tempfile.TemporaryDirectory() as temp_dir:
       # Test implementation
   ```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Run specific test with debug
python -m unittest tests.test_automated_token_generator.TestAutomatedKiteSystem.test_method_name -v
```

### Test Isolation

```python
def setUp(self):
    """Ensure each test runs in isolation"""
    # Reset global state
    # Clear caches
    # Initialize fresh data

def tearDown(self):
    """Clean up after each test"""
    # Restore original state
    # Clean up files
    # Reset mocks
```

## 📈 Performance Testing

### Load Testing

```python
def test_performance_under_load(self):
    """Test system performance under load"""
    import time
    
    start_time = time.time()
    
    # Simulate high load
    for i in range(1000):
        system.process_trade(mock_trade_data)
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Assert performance requirements
    self.assertLess(duration, 10.0)  # Should complete in under 10 seconds
```

### Memory Testing

```python
def test_memory_usage(self):
    """Test memory usage doesn't grow excessively"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    # Perform operations
    for i in range(100):
        system.process_trade(mock_trade_data)
    
    final_memory = process.memory_info().rss
    memory_growth = final_memory - initial_memory
    
    # Assert memory growth is reasonable
    self.assertLess(memory_growth, 50 * 1024 * 1024)  # Less than 50MB
```

## 🎯 Test Strategy

### Test Pyramid

1. **Unit Tests (70%)**: Fast, isolated, comprehensive
2. **Integration Tests (20%)**: Component interactions
3. **End-to-End Tests (10%)**: Full system workflows

### Test Priorities

1. **Critical Path**: Core trading functionality
2. **Security**: Credential handling and validation
3. **Error Handling**: Edge cases and failures
4. **Performance**: Response times and memory usage
5. **Usability**: User experience and notifications

### Test Maintenance

- **Regular Updates**: Keep tests current with code changes
- **Refactoring**: Improve test structure and readability
- **Documentation**: Keep test documentation updated
- **Coverage**: Monitor and improve coverage metrics

---

**🎯 Goal**: Achieve comprehensive test coverage with fast, reliable, and maintainable tests that ensure the copy trading system works correctly under all conditions.

**📚 Resources**: 
- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [pytest documentation](https://docs.pytest.org/)
- [Mock documentation](https://docs.python.org/3/library/unittest.mock.html)
