#!/usr/bin/env python3
"""
Test Suite for Automated Token Generator
=======================================

Comprehensive tests for the automated token generation system.

Test Coverage:
- Credential validation
- Token generation workflow
- Trade monitoring functionality
- Notification system
- Error handling and edge cases
- Security features
"""

import unittest
import os
import sys
import json
import tempfile
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.automated_token_generator import AutomatedKiteSystem

class TestAutomatedKiteSystem(unittest.TestCase):
    """Test cases for AutomatedKiteSystem class"""
    
    def setUp(self):
        """Set up test environment with mock credentials"""
        # Mock environment variables
        self.test_env = {
            'AUTOMATED_USER_ID': 'test_user_id',
            'AUTOMATED_PASSWORD': 'test_password',
            'AUTOMATED_API_KEY': 'test_api_key',
            'AUTOMATED_API_SECRET': 'test_api_secret',
            'AUTOMATED_AUTH_SECRET': 'test_auth_secret',
            'TELEGRAM_BOT_TOKEN': 'test_bot_token',
            'TELEGRAM_CHAT_ID': 'test_chat_id'
        }
        
        # Patch environment variables
        self.env_patcher = patch.dict(os.environ, self.test_env)
        self.env_patcher.start()
        
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
        os.chdir(self.original_cwd)
        # Clean up test files
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_initialization_with_valid_credentials(self):
        """Test system initialization with valid credentials"""
        system = AutomatedKiteSystem()
        
        self.assertEqual(system.USER_ID, 'test_user_id')
        self.assertEqual(system.PASSWORD, 'test_password')
        self.assertEqual(system.API_KEY, 'test_api_key')
        self.assertEqual(system.API_SECRET, 'test_api_secret')
        self.assertEqual(system.AUTH_SECRET, 'test_auth_secret')
        self.assertEqual(system.TELEGRAM_TOKEN, 'test_bot_token')
        self.assertEqual(system.TELEGRAM_CHAT_ID, 'test_chat_id')
    
    def test_initialization_with_missing_credentials(self):
        """Test system initialization with missing credentials"""
        # Remove one credential
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                AutomatedKiteSystem()
            
            self.assertIn("Missing required credentials", str(context.exception))
    
    def test_validate_credentials_success(self):
        """Test credential validation with valid credentials"""
        system = AutomatedKiteSystem()
        # Should not raise any exception
        self.assertTrue(True)
    
    def test_validate_credentials_failure(self):
        """Test credential validation with missing credentials"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                AutomatedKiteSystem()
    
    @patch('utils.automated_token_generator.pyotp.TOTP')
    def test_otp_generation(self, mock_totp):
        """Test OTP generation"""
        # Mock TOTP
        mock_totp_instance = Mock()
        mock_totp_instance.now.return_value = '123456'
        mock_totp.return_value = mock_totp_instance
        
        system = AutomatedKiteSystem()
        
        # Test OTP generation
        totp = pyotp.TOTP(system.AUTH_SECRET)
        otp = totp.now()
        
        self.assertEqual(otp, '123456')
        mock_totp.assert_called_once_with(system.AUTH_SECRET)
    
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
    
    @patch('utils.automated_token_generator.requests.post')
    def test_send_trade_notification_failure(self, mock_post):
        """Test failed trade notification"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        system = AutomatedKiteSystem()
        result = system.send_trade_notification("Test message")
        
        self.assertFalse(result)
        mock_post.assert_called_once()
    
    def test_send_trade_notification_no_credentials(self):
        """Test trade notification without Telegram credentials"""
        # Create system without Telegram credentials
        with patch.dict(os.environ, {k: v for k, v in self.test_env.items() 
                                   if not k.startswith('TELEGRAM')}):
            system = AutomatedKiteSystem()
            result = system.send_trade_notification("Test message")
            
            self.assertFalse(result)
    
    def test_format_trade_message_buy(self):
        """Test trade message formatting for BUY orders"""
        system = AutomatedKiteSystem()
        
        order = {
            'tradingsymbol': 'RELIANCE',
            'transaction_type': 'BUY',
            'quantity': 100,
            'price': 2500.50
        }
        
        message = system.format_trade_message(order)
        
        self.assertIn('🟢', message)
        self.assertIn('BUY', message)
        self.assertIn('RELIANCE', message)
        self.assertIn('100', message)
        self.assertIn('2500.50', message)
        self.assertIn('250,050.00', message)  # Total calculation
    
    def test_format_trade_message_sell(self):
        """Test trade message formatting for SELL orders"""
        system = AutomatedKiteSystem()
        
        order = {
            'tradingsymbol': 'TCS',
            'transaction_type': 'SELL',
            'quantity': 50,
            'price': 3500.75
        }
        
        message = system.format_trade_message(order)
        
        self.assertIn('🔴', message)
        self.assertIn('SELL', message)
        self.assertIn('TCS', message)
        self.assertIn('50', message)
        self.assertIn('3500.75', message)
        self.assertIn('175,037.50', message)  # Total calculation
    
    def test_format_trade_message_with_average_price(self):
        """Test trade message formatting with average price"""
        system = AutomatedKiteSystem()
        
        order = {
            'tradingsymbol': 'INFY',
            'transaction_type': 'BUY',
            'quantity': 25,
            'price': 0,  # No price
            'average_price': 1500.25
        }
        
        message = system.format_trade_message(order)
        
        self.assertIn('1500.25', message)
        self.assertIn('37,506.25', message)  # Total calculation with average price
    
    def test_format_trade_message_error_handling(self):
        """Test trade message formatting error handling"""
        system = AutomatedKiteSystem()
        
        # Test with invalid order data
        order = {}
        message = system.format_trade_message(order)
        
        self.assertIn('Trade Alert', message)
        self.assertIn('N/A', message)
    
    def test_generate_order_id(self):
        """Test order ID generation"""
        system = AutomatedKiteSystem()
        
        order = {
            'order_id': '12345',
            'status': 'COMPLETE',
            'tradingsymbol': 'RELIANCE'
        }
        
        order_id = system.generate_order_id(order)
        
        self.assertIsInstance(order_id, str)
        self.assertEqual(len(order_id), 12)  # MD5 hash truncated to 12 chars
    
    def test_generate_order_id_consistency(self):
        """Test order ID generation consistency"""
        system = AutomatedKiteSystem()
        
        order = {
            'order_id': '12345',
            'status': 'COMPLETE',
            'tradingsymbol': 'RELIANCE'
        }
        
        # Generate ID multiple times
        id1 = system.generate_order_id(order)
        id2 = system.generate_order_id(order)
        
        self.assertEqual(id1, id2)  # Should be consistent
    
    @patch('utils.automated_token_generator.KiteConnect')
    def test_monitor_trades_success(self, mock_kite_connect):
        """Test successful trade monitoring"""
        # Mock KiteConnect instance
        mock_kite = Mock()
        mock_kite.orders.return_value = [
            {
                'order_id': '12345',
                'status': 'COMPLETE',
                'tradingsymbol': 'RELIANCE',
                'transaction_type': 'BUY',
                'quantity': 100,
                'price': 2500.50
            }
        ]
        mock_kite_connect.return_value = mock_kite
        
        system = AutomatedKiteSystem()
        system.kite = mock_kite
        
        # Mock notification method
        with patch.object(system, 'send_trade_notification', return_value=True):
            system.monitor_trades()
            
            # Check if order was processed
            self.assertEqual(len(system.processed_orders), 1)
            mock_kite.orders.assert_called_once()
    
    @patch('utils.automated_token_generator.KiteConnect')
    def test_monitor_trades_duplicate_prevention(self, mock_kite_connect):
        """Test duplicate order prevention"""
        # Mock KiteConnect instance
        mock_kite = Mock()
        mock_kite.orders.return_value = [
            {
                'order_id': '12345',
                'status': 'COMPLETE',
                'tradingsymbol': 'RELIANCE',
                'transaction_type': 'BUY',
                'quantity': 100,
                'price': 2500.50
            }
        ]
        mock_kite_connect.return_value = mock_kite
        
        system = AutomatedKiteSystem()
        system.kite = mock_kite
        
        # Mock notification method
        with patch.object(system, 'send_trade_notification', return_value=True):
            # Process the same order twice
            system.monitor_trades()
            system.monitor_trades()
            
            # Should only process once
            self.assertEqual(len(system.processed_orders), 1)
    
    @patch('utils.automated_token_generator.KiteConnect')
    def test_monitor_trades_memory_cleanup(self, mock_kite_connect):
        """Test memory cleanup for processed orders"""
        # Mock KiteConnect instance
        mock_kite = Mock()
        mock_kite.orders.return_value = []
        mock_kite_connect.return_value = mock_kite
        
        system = AutomatedKiteSystem()
        system.kite = mock_kite
        
        # Add many processed orders
        for i in range(60):
            system.processed_orders.add(f"order_{i}")
        
        self.assertEqual(len(system.processed_orders), 60)
        
        # Monitor trades should trigger cleanup
        system.monitor_trades()
        
        # Should be cleaned up to 25 items
        self.assertEqual(len(system.processed_orders), 25)
    
    def test_monitor_trades_no_kite_client(self):
        """Test trade monitoring without Kite client"""
        system = AutomatedKiteSystem()
        system.kite = None
        
        # Should not raise exception
        system.monitor_trades()
    
    @patch('utils.automated_token_generator.KiteConnect')
    def test_monitor_trades_api_error(self, mock_kite_connect):
        """Test trade monitoring with API error"""
        # Mock KiteConnect instance that raises exception
        mock_kite = Mock()
        mock_kite.orders.side_effect = Exception("API Error")
        mock_kite_connect.return_value = mock_kite
        
        system = AutomatedKiteSystem()
        system.kite = mock_kite
        
        # Should not raise exception
        system.monitor_trades()
    
    def test_trade_count_increment(self):
        """Test trade count increment"""
        system = AutomatedKiteSystem()
        
        # Initial count should be 0
        self.assertEqual(system.trade_count, 0)
        
        # Format a trade message (increments count)
        order = {
            'tradingsymbol': 'RELIANCE',
            'transaction_type': 'BUY',
            'quantity': 100,
            'price': 2500.50
        }
        
        system.format_trade_message(order)
        self.assertEqual(system.trade_count, 1)
        
        system.format_trade_message(order)
        self.assertEqual(system.trade_count, 2)

class TestAutomatedTokenGeneration(unittest.TestCase):
    """Test cases for automated token generation functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_env = {
            'AUTOMATED_USER_ID': 'test_user_id',
            'AUTOMATED_PASSWORD': 'test_password',
            'AUTOMATED_API_KEY': 'test_api_key',
            'AUTOMATED_API_SECRET': 'test_api_secret',
            'AUTOMATED_AUTH_SECRET': 'test_auth_secret',
            'TELEGRAM_BOT_TOKEN': 'test_bot_token',
            'TELEGRAM_CHAT_ID': 'test_chat_id'
        }
        
        self.env_patcher = patch.dict(os.environ, self.test_env)
        self.env_patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
    
    @patch('utils.automated_token_generator.webdriver.Chrome')
    @patch('utils.automated_token_generator.KiteConnect')
    def test_automated_token_generation_success(self, mock_kite_connect, mock_chrome):
        """Test successful automated token generation"""
        # Mock WebDriver
        mock_driver = Mock()
        mock_driver.current_url = "https://kite.zerodha.com/connect/login?request_token=test_token"
        mock_chrome.return_value = mock_driver
        
        # Mock WebDriverWait and elements
        with patch('utils.automated_token_generator.WebDriverWait') as mock_wait:
            mock_element = Mock()
            mock_wait.return_value.until.return_value = mock_element
            
            # Mock KiteConnect
            mock_kite = Mock()
            mock_kite.generate_session.return_value = {"access_token": "test_access_token"}
            mock_kite_connect.return_value = mock_kite
            
            system = AutomatedKiteSystem()
            result = system.automated_token_generation()
            
            self.assertEqual(result, "test_access_token")
            mock_driver.get.assert_called_once()
            mock_driver.quit.assert_called_once()
    
    @patch('utils.automated_token_generator.webdriver.Chrome')
    def test_automated_token_generation_failure(self, mock_chrome):
        """Test failed automated token generation"""
        # Mock WebDriver that raises exception
        mock_chrome.side_effect = Exception("Chrome error")
        
        system = AutomatedKiteSystem()
        result = system.automated_token_generation()
        
        self.assertIsNone(result)
    
    @patch('utils.automated_token_generator.webdriver.Chrome')
    def test_automated_token_generation_no_token(self, mock_chrome):
        """Test automated token generation with no request token"""
        # Mock WebDriver
        mock_driver = Mock()
        mock_driver.current_url = "https://kite.zerodha.com/connect/login"  # No request_token
        mock_chrome.return_value = mock_driver
        
        # Mock WebDriverWait and elements
        with patch('utils.automated_token_generator.WebDriverWait') as mock_wait:
            mock_element = Mock()
            mock_wait.return_value.until.return_value = mock_element
            
            system = AutomatedKiteSystem()
            result = system.automated_token_generation()
            
            self.assertIsNone(result)
            mock_driver.quit.assert_called_once()

class TestIntegration(unittest.TestCase):
    """Integration tests for the automated system"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_env = {
            'AUTOMATED_USER_ID': 'test_user_id',
            'AUTOMATED_PASSWORD': 'test_password',
            'AUTOMATED_API_KEY': 'test_api_key',
            'AUTOMATED_API_SECRET': 'test_api_secret',
            'AUTOMATED_AUTH_SECRET': 'test_auth_secret',
            'TELEGRAM_BOT_TOKEN': 'test_bot_token',
            'TELEGRAM_CHAT_ID': 'test_chat_id'
        }
        
        self.env_patcher = patch.dict(os.environ, self.test_env)
        self.env_patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
    
    @patch('utils.automated_token_generator.webdriver.Chrome')
    @patch('utils.automated_token_generator.KiteConnect')
    @patch('utils.automated_token_generator.requests.post')
    def test_full_workflow_simulation(self, mock_post, mock_kite_connect, mock_chrome):
        """Test complete workflow simulation"""
        # Mock successful token generation
        mock_driver = Mock()
        mock_driver.current_url = "https://kite.zerodha.com/connect/login?request_token=test_token"
        mock_chrome.return_value = mock_driver
        
        with patch('utils.automated_token_generator.WebDriverWait') as mock_wait:
            mock_element = Mock()
            mock_wait.return_value.until.return_value = mock_element
            
            # Mock KiteConnect
            mock_kite = Mock()
            mock_kite.generate_session.return_value = {"access_token": "test_access_token"}
            mock_kite.orders.return_value = [
                {
                    'order_id': '12345',
                    'status': 'COMPLETE',
                    'tradingsymbol': 'RELIANCE',
                    'transaction_type': 'BUY',
                    'quantity': 100,
                    'price': 2500.50
                }
            ]
            mock_kite_connect.return_value = mock_kite
            
            # Mock Telegram notification
            mock_response = Mock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response
            
            system = AutomatedKiteSystem()
            
            # Test token generation
            token = system.automated_token_generation()
            self.assertEqual(token, "test_access_token")
            
            # Test trade monitoring
            system.kite = mock_kite
            system.monitor_trades()
            
            # Verify notification was sent
            self.assertEqual(mock_post.call_count, 1)
            self.assertEqual(len(system.processed_orders), 1)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
