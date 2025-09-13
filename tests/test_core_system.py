#!/usr/bin/env python3
"""
Test Suite for Core Trading System
==================================

Comprehensive tests for the core trading system components.

Test Coverage:
- Configuration management
- Master client functionality
- Follower client functionality
- Notification system
- System integration
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

from core.config import SecureConfigManager, AccountConfig
from core.notifications import NotificationManager, NotificationConfig

class TestAccountConfig(unittest.TestCase):
    """Test cases for AccountConfig class"""
    
    def test_account_config_initialization(self):
        """Test AccountConfig initialization with default values"""
        config = AccountConfig(
            api_key="test_key",
            api_secret="test_secret",
            access_token="test_token",
            user_id="test_user"
        )
        
        self.assertEqual(config.api_key, "test_key")
        self.assertEqual(config.api_secret, "test_secret")
        self.assertEqual(config.access_token, "test_token")
        self.assertEqual(config.user_id, "test_user")
        self.assertEqual(config.multiplier, 1.0)
        self.assertEqual(config.max_position_size, 1000)
        self.assertTrue(config.enabled)
    
    def test_account_config_with_custom_values(self):
        """Test AccountConfig initialization with custom values"""
        config = AccountConfig(
            api_key="test_key",
            api_secret="test_secret",
            access_token="test_token",
            user_id="test_user",
            multiplier=0.5,
            max_position_size=500,
            enabled=False
        )
        
        self.assertEqual(config.multiplier, 0.5)
        self.assertEqual(config.max_position_size, 500)
        self.assertFalse(config.enabled)
    
    def test_account_config_default_segments(self):
        """Test AccountConfig default segment configuration"""
        config = AccountConfig(
            api_key="test_key",
            api_secret="test_secret",
            access_token="test_token",
            user_id="test_user"
        )
        
        expected_segments = ['NSE', 'BSE', 'NFO', 'MCX', 'BFO', 'CDS']
        self.assertEqual(config.enabled_segments, expected_segments)
        
        # Check segment multipliers
        for segment in expected_segments:
            self.assertEqual(config.segment_multipliers[segment], 1.0)
        
        # Check segment limits
        self.assertEqual(config.segment_limits['NSE'], 1000)
        self.assertEqual(config.segment_limits['NFO'], 500)  # Half of max_position_size
        self.assertEqual(config.segment_limits['MCX'], 200)  # One-fifth of max_position_size

class TestSecureConfigManager(unittest.TestCase):
    """Test cases for SecureConfigManager class"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_env = {
            'MASTER_API_KEY': 'master_key',
            'MASTER_API_SECRET': 'master_secret',
            'MASTER_ACCESS_TOKEN': 'master_token',
            'MASTER_USER_ID': 'master_user',
            'FOLLOWER_COUNT': '2',
            'FOLLOWER_1_API_KEY': 'follower1_key',
            'FOLLOWER_1_API_SECRET': 'follower1_secret',
            'FOLLOWER_1_ACCESS_TOKEN': 'follower1_token',
            'FOLLOWER_1_USER_ID': 'follower1_user',
            'FOLLOWER_1_MULTIPLIER': '0.5',
            'FOLLOWER_1_MAX_POSITION': '500',
            'FOLLOWER_1_ENABLED': 'True',
            'FOLLOWER_2_API_KEY': 'follower2_key',
            'FOLLOWER_2_API_SECRET': 'follower2_secret',
            'FOLLOWER_2_ACCESS_TOKEN': 'follower2_token',
            'FOLLOWER_2_USER_ID': 'follower2_user',
            'FOLLOWER_2_MULTIPLIER': '0.8',
            'FOLLOWER_2_MAX_POSITION': '800',
            'FOLLOWER_2_ENABLED': 'False'
        }
        
        self.env_patcher = patch.dict(os.environ, self.test_env)
        self.env_patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.env_patcher.stop()
    
    def test_load_master_config(self):
        """Test loading master account configuration"""
        config_manager = SecureConfigManager()
        master_config = config_manager.load_master_config()
        
        self.assertEqual(master_config.api_key, 'master_key')
        self.assertEqual(master_config.api_secret, 'master_secret')
        self.assertEqual(master_config.access_token, 'master_token')
        self.assertEqual(master_config.user_id, 'master_user')
        self.assertEqual(master_config.multiplier, 1.0)
    
    def test_load_follower_configs(self):
        """Test loading follower account configurations"""
        config_manager = SecureConfigManager()
        follower_configs = config_manager.load_follower_configs()
        
        self.assertEqual(len(follower_configs), 2)
        
        # Check first follower
        follower1 = follower_configs[0]
        self.assertEqual(follower1.api_key, 'follower1_key')
        self.assertEqual(follower1.user_id, 'follower1_user')
        self.assertEqual(follower1.multiplier, 0.5)
        self.assertEqual(follower1.max_position_size, 500)
        self.assertTrue(follower1.enabled)
        
        # Check second follower
        follower2 = follower_configs[1]
        self.assertEqual(follower2.api_key, 'follower2_key')
        self.assertEqual(follower2.user_id, 'follower2_user')
        self.assertEqual(follower2.multiplier, 0.8)
        self.assertEqual(follower2.max_position_size, 800)
        self.assertFalse(follower2.enabled)
    
    def test_load_follower_configs_with_segment_settings(self):
        """Test loading follower configs with segment-specific settings"""
        test_env = self.test_env.copy()
        test_env.update({
            'FOLLOWER_1_NSE_MULTIPLIER': '0.3',
            'FOLLOWER_1_NFO_MULTIPLIER': '0.1',
            'FOLLOWER_1_MCX_LIMIT': '100',
            'FOLLOWER_1_ENABLED_SEGMENTS': 'NSE,NFO'
        })
        
        with patch.dict(os.environ, test_env):
            config_manager = SecureConfigManager()
            follower_configs = config_manager.load_follower_configs()
            
            follower1 = follower_configs[0]
            self.assertEqual(follower1.segment_multipliers['NSE'], 0.3)
            self.assertEqual(follower1.segment_multipliers['NFO'], 0.1)
            self.assertEqual(follower1.segment_limits['MCX'], 100)
            self.assertEqual(follower1.enabled_segments, ['NSE', 'NFO'])
    
    def test_validate_account_config(self):
        """Test account configuration validation"""
        config_manager = SecureConfigManager()
        
        # Valid config
        valid_config = AccountConfig(
            api_key="test_key",
            api_secret="test_secret",
            access_token="test_token",
            user_id="test_user"
        )
        self.assertTrue(config_manager._validate_account_config(valid_config))
        
        # Invalid config (empty fields)
        invalid_config = AccountConfig(
            api_key="",
            api_secret="test_secret",
            access_token="test_token",
            user_id="test_user"
        )
        self.assertFalse(config_manager._validate_account_config(invalid_config))
    
    def test_get_system_config(self):
        """Test system configuration retrieval"""
        config_manager = SecureConfigManager()
        system_config = config_manager.get_system_config()
        
        self.assertIn('check_interval', system_config)
        self.assertIn('max_retries', system_config)
        self.assertIn('log_level', system_config)
        self.assertIn('paper_trading', system_config)
        self.assertIn('max_daily_trades', system_config)
        self.assertIn('risk_management_enabled', system_config)
    
    def test_create_sample_config_file(self):
        """Test sample configuration file creation"""
        config_manager = SecureConfigManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                config_manager.create_sample_config_file()
                
                # Check if file was created
                self.assertTrue(os.path.exists('config.json.sample'))
                
                # Check file content
                with open('config.json.sample', 'r') as f:
                    config_data = json.load(f)
                
                self.assertIn('followers', config_data)
                self.assertIsInstance(config_data['followers'], list)
                self.assertEqual(len(config_data['followers']), 1)
                
            finally:
                os.chdir(original_cwd)

class TestNotificationConfig(unittest.TestCase):
    """Test cases for NotificationConfig class"""
    
    def test_notification_config_defaults(self):
        """Test NotificationConfig default values"""
        config = NotificationConfig()
        
        self.assertFalse(config.whatsapp_enabled)
        self.assertFalse(config.telegram_enabled)
        self.assertFalse(config.email_enabled)
        self.assertFalse(config.discord_enabled)
        self.assertEqual(config.smtp_port, 587)

class TestNotificationManager(unittest.TestCase):
    """Test cases for NotificationManager class"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_config = NotificationConfig(
            telegram_enabled=True,
            telegram_bot_token="test_bot_token",
            telegram_chat_id="test_chat_id"
        )
    
    @patch('core.notifications.requests.post')
    def test_send_telegram_notification_success(self, mock_post):
        """Test successful Telegram notification"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        manager = NotificationManager(self.test_config)
        result = manager.send_telegram_notification("Test message")
        
        self.assertTrue(result)
        mock_post.assert_called_once()
    
    @patch('core.notifications.requests.post')
    def test_send_telegram_notification_failure(self, mock_post):
        """Test failed Telegram notification"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response
        
        manager = NotificationManager(self.test_config)
        result = manager.send_telegram_notification("Test message")
        
        self.assertFalse(result)
    
    def test_send_telegram_notification_disabled(self):
        """Test Telegram notification when disabled"""
        config = NotificationConfig(telegram_enabled=False)
        manager = NotificationManager(config)
        result = manager.send_telegram_notification("Test message")
        
        self.assertFalse(result)
    
    @patch('core.notifications.smtplib.SMTP')
    def test_send_email_notification_success(self, mock_smtp):
        """Test successful email notification"""
        config = NotificationConfig(
            email_enabled=True,
            smtp_server="smtp.gmail.com",
            smtp_port=587,
            email_user="test@gmail.com",
            email_password="test_password",
            email_to="recipient@gmail.com"
        )
        
        manager = NotificationManager(config)
        result = manager.send_email_notification("Test subject", "Test message")
        
        self.assertTrue(result)
        mock_smtp.assert_called_once()
    
    def test_send_email_notification_disabled(self):
        """Test email notification when disabled"""
        config = NotificationConfig(email_enabled=False)
        manager = NotificationManager(config)
        result = manager.send_email_notification("Test subject", "Test message")
        
        self.assertFalse(result)
    
    def test_send_trade_notification(self):
        """Test trade notification formatting and sending"""
        manager = NotificationManager(self.test_config)
        
        trade_data = {
            'tradingsymbol': 'RELIANCE',
            'transaction_type': 'BUY',
            'quantity': 100,
            'price': 2500.50
        }
        
        follower_results = [
            {
                'user_id': 'follower1',
                'success': True,
                'replicated_quantity': 50,
                'error': ''
            }
        ]
        
        with patch.object(manager, 'send_telegram_notification', return_value=True) as mock_send:
            result = manager.send_trade_notification(trade_data, follower_results)
            
            self.assertTrue(result)
            mock_send.assert_called_once()
            
            # Check if message contains trade details
            call_args = mock_send.call_args[0][0]
            self.assertIn('RELIANCE', call_args)
            self.assertIn('BUY', call_args)
            self.assertIn('100', call_args)
    
    def test_send_system_alert(self):
        """Test system alert notification"""
        manager = NotificationManager(self.test_config)
        
        with patch.object(manager, 'send_telegram_notification', return_value=True) as mock_send:
            result = manager.send_system_alert("Test Alert", "Test message", "INFO")
            
            self.assertTrue(result)
            mock_send.assert_called_once()
            
            # Check if message contains alert details
            call_args = mock_send.call_args[0][0]
            self.assertIn('Test Alert', call_args)
            self.assertIn('Test message', call_args)
            self.assertIn('INFO', call_args)
    
    def test_send_daily_summary(self):
        """Test daily summary notification"""
        manager = NotificationManager(self.test_config)
        
        summary_data = {
            'total_trades': 10,
            'successful_copies': 8,
            'failed_copies': 2,
            'followers': ['follower1', 'follower2'],
            'uptime': '8:30:00'
        }
        
        with patch.object(manager, 'send_telegram_notification', return_value=True) as mock_send:
            result = manager.send_daily_summary(summary_data)
            
            self.assertTrue(result)
            mock_send.assert_called_once()
            
            # Check if message contains summary details
            call_args = mock_send.call_args[0][0]
            self.assertIn('10', call_args)  # total_trades
            self.assertIn('8', call_args)   # successful_copies
            self.assertIn('2', call_args)   # failed_copies

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
