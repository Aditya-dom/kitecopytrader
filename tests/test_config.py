#!/usr/bin/env python3
"""
Test Configuration for Zerodha Copy Trading System
================================================

Centralized configuration for all test suites.

Features:
- Test environment setup
- Mock data configuration
- Test database setup
- Environment variable management
- Test utilities and helpers
"""

import os
import sys
import tempfile
import json
from unittest.mock import Mock, MagicMock

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestConfig:
    """Configuration class for tests"""
    
    # Test environment variables
    TEST_ENV_VARS = {
        # Master account
        'MASTER_API_KEY': 'test_master_api_key',
        'MASTER_API_SECRET': 'test_master_api_secret',
        'MASTER_ACCESS_TOKEN': 'test_master_access_token',
        'MASTER_USER_ID': 'test_master_user_id',
        
        # Follower accounts
        'FOLLOWER_COUNT': '2',
        'FOLLOWER_1_API_KEY': 'test_follower1_api_key',
        'FOLLOWER_1_API_SECRET': 'test_follower1_api_secret',
        'FOLLOWER_1_ACCESS_TOKEN': 'test_follower1_access_token',
        'FOLLOWER_1_USER_ID': 'test_follower1_user_id',
        'FOLLOWER_1_MULTIPLIER': '0.5',
        'FOLLOWER_1_MAX_POSITION': '500',
        'FOLLOWER_1_ENABLED': 'True',
        
        'FOLLOWER_2_API_KEY': 'test_follower2_api_key',
        'FOLLOWER_2_API_SECRET': 'test_follower2_api_secret',
        'FOLLOWER_2_ACCESS_TOKEN': 'test_follower2_access_token',
        'FOLLOWER_2_USER_ID': 'test_follower2_user_id',
        'FOLLOWER_2_MULTIPLIER': '0.8',
        'FOLLOWER_2_MAX_POSITION': '800',
        'FOLLOWER_2_ENABLED': 'False',
        
        # Automated system
        'AUTOMATED_USER_ID': 'test_automated_user_id',
        'AUTOMATED_PASSWORD': 'test_automated_password',
        'AUTOMATED_API_KEY': 'test_automated_api_key',
        'AUTOMATED_API_SECRET': 'test_automated_api_secret',
        'AUTOMATED_AUTH_SECRET': 'test_automated_auth_secret',
        
        # Notifications
        'TELEGRAM_BOT_TOKEN': 'test_telegram_bot_token',
        'TELEGRAM_CHAT_ID': 'test_telegram_chat_id',
        'TWILIO_ACCOUNT_SID': 'test_twilio_account_sid',
        'TWILIO_AUTH_TOKEN': 'test_twilio_auth_token',
        'TWILIO_WHATSAPP_FROM': 'test_twilio_whatsapp_from',
        'WHATSAPP_TO': 'test_whatsapp_to',
        
        # System settings
        'PAPER_TRADING': 'True',
        'LOG_LEVEL': 'INFO',
        'CHECK_INTERVAL': '1',
        'MAX_RETRIES': '3',
        'MAX_DAILY_TRADES': '100',
        'RISK_MANAGEMENT': 'True'
    }
    
    # Mock data for testing
    MOCK_TRADE_DATA = {
        'order_id': '12345',
        'tradingsymbol': 'RELIANCE',
        'exchange': 'NSE',
        'transaction_type': 'BUY',
        'quantity': 100,
        'price': 2500.50,
        'average_price': 2500.50,
        'status': 'COMPLETE',
        'product': 'CNC',
        'order_type': 'MARKET',
        'timestamp': '2024-01-01 10:30:00'
    }
    
    MOCK_ORDER_DATA = {
        'order_id': '67890',
        'tradingsymbol': 'TCS',
        'exchange': 'NSE',
        'transaction_type': 'SELL',
        'quantity': 50,
        'price': 3500.75,
        'average_price': 3500.75,
        'status': 'EXECUTED',
        'product': 'CNC',
        'order_type': 'LIMIT',
        'timestamp': '2024-01-01 11:15:00'
    }
    
    MOCK_POSITION_DATA = {
        'tradingsymbol': 'RELIANCE',
        'exchange': 'NSE',
        'quantity': 100,
        'average_price': 2500.50,
        'pnl': 1500.00,
        'day_change': 2.5,
        'day_change_percentage': 0.1
    }
    
    MOCK_PROFILE_DATA = {
        'user_id': 'test_user_id',
        'user_name': 'Test User',
        'email': 'test@example.com',
        'broker': 'ZERODHA',
        'exchanges': ['NSE', 'BSE', 'NFO', 'MCX', 'BFO', 'CDS'],
        'products': ['CNC', 'MIS', 'NRML'],
        'order_types': ['MARKET', 'LIMIT', 'SL', 'SL-M']
    }
    
    # Test file paths
    TEST_CONFIG_FILE = 'test_config.json'
    TEST_LOG_FILE = 'test_copy_trader.log'
    TEST_ENV_FILE = 'test.env'
    
    @classmethod
    def setup_test_environment(cls):
        """Set up test environment with mock data"""
        # Set environment variables
        for key, value in cls.TEST_ENV_VARS.items():
            os.environ[key] = value
        
        # Create temporary directory for test files
        cls.test_dir = tempfile.mkdtemp()
        cls.original_cwd = os.getcwd()
        os.chdir(cls.test_dir)
        
        return cls.test_dir
    
    @classmethod
    def cleanup_test_environment(cls):
        """Clean up test environment"""
        # Restore original working directory
        if hasattr(cls, 'original_cwd'):
            os.chdir(cls.original_cwd)
        
        # Clean up test directory
        if hasattr(cls, 'test_dir'):
            import shutil
            shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    @classmethod
    def create_test_config_file(cls, filename=None):
        """Create a test configuration file"""
        if filename is None:
            filename = cls.TEST_CONFIG_FILE
        
        config_data = {
            "followers": [
                {
                    "api_key": cls.TEST_ENV_VARS['FOLLOWER_1_API_KEY'],
                    "api_secret": cls.TEST_ENV_VARS['FOLLOWER_1_API_SECRET'],
                    "access_token": cls.TEST_ENV_VARS['FOLLOWER_1_ACCESS_TOKEN'],
                    "user_id": cls.TEST_ENV_VARS['FOLLOWER_1_USER_ID'],
                    "multiplier": float(cls.TEST_ENV_VARS['FOLLOWER_1_MULTIPLIER']),
                    "max_position_size": int(cls.TEST_ENV_VARS['FOLLOWER_1_MAX_POSITION']),
                    "enabled": cls.TEST_ENV_VARS['FOLLOWER_1_ENABLED'].lower() == 'true'
                },
                {
                    "api_key": cls.TEST_ENV_VARS['FOLLOWER_2_API_KEY'],
                    "api_secret": cls.TEST_ENV_VARS['FOLLOWER_2_API_SECRET'],
                    "access_token": cls.TEST_ENV_VARS['FOLLOWER_2_ACCESS_TOKEN'],
                    "user_id": cls.TEST_ENV_VARS['FOLLOWER_2_USER_ID'],
                    "multiplier": float(cls.TEST_ENV_VARS['FOLLOWER_2_MULTIPLIER']),
                    "max_position_size": int(cls.TEST_ENV_VARS['FOLLOWER_2_MAX_POSITION']),
                    "enabled": cls.TEST_ENV_VARS['FOLLOWER_2_ENABLED'].lower() == 'true'
                }
            ]
        }
        
        with open(filename, 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return filename
    
    @classmethod
    def create_mock_kite_client(cls):
        """Create a mock KiteConnect client"""
        mock_kite = Mock()
        
        # Mock profile method
        mock_kite.profile.return_value = cls.MOCK_PROFILE_DATA
        
        # Mock orders method
        mock_kite.orders.return_value = [cls.MOCK_TRADE_DATA, cls.MOCK_ORDER_DATA]
        
        # Mock positions method
        mock_kite.positions.return_value = {
            'day': [cls.MOCK_POSITION_DATA],
            'net': []
        }
        
        # Mock generate_session method
        mock_kite.generate_session.return_value = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token'
        }
        
        return mock_kite
    
    @classmethod
    def create_mock_webdriver(cls):
        """Create a mock WebDriver for automated tests"""
        mock_driver = Mock()
        
        # Mock WebDriver methods
        mock_driver.get.return_value = None
        mock_driver.current_url = "https://kite.zerodha.com/connect/login?request_token=test_token"
        mock_driver.quit.return_value = None
        
        # Mock WebDriverWait
        mock_element = Mock()
        mock_element.send_keys.return_value = None
        mock_element.clear.return_value = None
        
        return mock_driver, mock_element
    
    @classmethod
    def create_mock_requests_response(cls, status_code=200, content=None):
        """Create a mock requests response"""
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.content = content or b'{"status": "success"}'
        mock_response.json.return_value = {"status": "success"}
        return mock_response

class TestHelpers:
    """Helper functions for tests"""
    
    @staticmethod
    def assert_trade_data_valid(trade_data):
        """Assert that trade data contains required fields"""
        required_fields = ['order_id', 'tradingsymbol', 'transaction_type', 'quantity']
        for field in required_fields:
            assert field in trade_data, f"Missing required field: {field}"
    
    @staticmethod
    def assert_notification_sent(mock_send, expected_content=None):
        """Assert that a notification was sent"""
        assert mock_send.called, "Notification was not sent"
        if expected_content:
            call_args = mock_send.call_args[0][0]
            assert expected_content in call_args, f"Expected content '{expected_content}' not found in notification"
    
    @staticmethod
    def create_test_order(tradingsymbol='TEST', transaction_type='BUY', quantity=100, price=1000.0):
        """Create a test order with specified parameters"""
        return {
            'order_id': f'TEST_{tradingsymbol}_{transaction_type}',
            'tradingsymbol': tradingsymbol,
            'exchange': 'NSE',
            'transaction_type': transaction_type,
            'quantity': quantity,
            'price': price,
            'average_price': price,
            'status': 'COMPLETE',
            'product': 'CNC',
            'order_type': 'MARKET',
            'timestamp': '2024-01-01 10:30:00'
        }
    
    @staticmethod
    def create_test_follower_config(user_id='test_follower', multiplier=1.0, enabled=True):
        """Create a test follower configuration"""
        return {
            'api_key': f'{user_id}_api_key',
            'api_secret': f'{user_id}_api_secret',
            'access_token': f'{user_id}_access_token',
            'user_id': user_id,
            'multiplier': multiplier,
            'max_position_size': 1000,
            'enabled': enabled
        }

# Test data generators
class TestDataGenerator:
    """Generate test data for various scenarios"""
    
    @staticmethod
    def generate_trade_sequence(count=5):
        """Generate a sequence of test trades"""
        trades = []
        symbols = ['RELIANCE', 'TCS', 'INFY', 'HDFC', 'ICICIBANK']
        
        for i in range(count):
            trade = TestConfig.MOCK_TRADE_DATA.copy()
            trade['order_id'] = f'TEST_{i+1:03d}'
            trade['tradingsymbol'] = symbols[i % len(symbols)]
            trade['transaction_type'] = 'BUY' if i % 2 == 0 else 'SELL'
            trade['quantity'] = (i + 1) * 10
            trade['price'] = 1000 + (i * 100)
            trade['timestamp'] = f'2024-01-01 {10 + i}:30:00'
            trades.append(trade)
        
        return trades
    
    @staticmethod
    def generate_follower_configs(count=3):
        """Generate multiple follower configurations"""
        configs = []
        
        for i in range(count):
            config = TestConfig.MOCK_PROFILE_DATA.copy()
            config['user_id'] = f'follower_{i+1}'
            config['multiplier'] = 0.5 + (i * 0.2)
            config['enabled'] = i % 2 == 0
            configs.append(config)
        
        return configs
    
    @staticmethod
    def generate_error_scenarios():
        """Generate various error scenarios for testing"""
        return {
            'network_error': Exception("Network connection failed"),
            'api_error': Exception("API rate limit exceeded"),
            'authentication_error': Exception("Invalid credentials"),
            'timeout_error': Exception("Request timeout"),
            'validation_error': ValueError("Invalid input data")
        }

if __name__ == '__main__':
    # Test the configuration
    print("Testing configuration setup...")
    
    # Setup test environment
    test_dir = TestConfig.setup_test_environment()
    print(f"Test directory created: {test_dir}")
    
    # Create test config file
    config_file = TestConfig.create_test_config_file()
    print(f"Test config file created: {config_file}")
    
    # Create mock data
    mock_kite = TestConfig.create_mock_kite_client()
    print("Mock KiteConnect client created")
    
    # Generate test data
    trades = TestDataGenerator.generate_trade_sequence(3)
    print(f"Generated {len(trades)} test trades")
    
    # Cleanup
    TestConfig.cleanup_test_environment()
    print("Test environment cleaned up")
    
    print("✅ Configuration test completed successfully!")
