#!/usr/bin/env python3
"""
Configuration Loader Utility
============================

Utility to load configuration from JSON files and environment variables.
Supports both the simple kite_config.json format and the complete configuration format.

Features:
- JSON configuration file loading
- Environment variable fallback
- Configuration validation
- Multiple configuration formats support
- Secure credential handling
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class KiteCredentials:
    """Kite credentials configuration"""
    user_id: str
    password: str
    api_key: str
    api_secret: str
    auth_secret: str
    access_token: str

@dataclass
class TelegramConfig:
    """Telegram configuration"""
    bot_token: str
    chat_id: str

@dataclass
class FollowerConfig:
    """Follower account configuration"""
    api_key: str
    api_secret: str
    access_token: str
    user_id: str
    multiplier: float = 1.0
    max_position_size: int = 1000
    enabled: bool = True
    enabled_segments: List[str] = None
    segment_multipliers: Dict[str, float] = None
    segment_limits: Dict[str, int] = None

@dataclass
class SystemConfig:
    """System configuration"""
    paper_trading: bool = True
    log_level: str = "INFO"
    check_interval: int = 1
    max_retries: int = 3
    max_daily_trades: int = 100
    risk_management_enabled: bool = True
    auto_token_refresh: bool = True
    market_hours_only: bool = True

class ConfigLoader:
    """Configuration loader with support for multiple formats"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config_data = {}
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file and environment variables"""
        # Try to load from JSON file first
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config_data = json.load(f)
                logger.info(f"Configuration loaded from {self.config_file}")
            except Exception as e:
                logger.error(f"Error loading config file: {e}")
                self.config_data = {}
        
        # Override with environment variables
        self._load_from_environment()
        
        return self.config_data
    
    def _load_from_environment(self):
        """Load configuration from environment variables"""
        # Kite credentials
        kite_env = {
            'user_id': os.getenv('KITE_USER_ID'),
            'password': os.getenv('KITE_PASSWORD'),
            'api_key': os.getenv('KITE_API_KEY'),
            'api_secret': os.getenv('KITE_API_SECRET'),
            'auth_secret': os.getenv('KITE_AUTH_SECRET'),
            'access_token': os.getenv('KITE_ACCESS_TOKEN')
        }
        
        # Only add kite section if any kite env vars are set
        if any(kite_env.values()):
            if 'kite' not in self.config_data:
                self.config_data['kite'] = {}
            self.config_data['kite'].update({k: v for k, v in kite_env.items() if v})
        
        # Telegram credentials
        telegram_env = {
            'bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
            'chat_id': os.getenv('TELEGRAM_CHAT_ID')
        }
        
        if any(telegram_env.values()):
            if 'telegram' not in self.config_data:
                self.config_data['telegram'] = {}
            self.config_data['telegram'].update({k: v for k, v in telegram_env.items() if v})
        
        # Master account (for copy trading)
        master_env = {
            'api_key': os.getenv('MASTER_API_KEY'),
            'api_secret': os.getenv('MASTER_API_SECRET'),
            'access_token': os.getenv('MASTER_ACCESS_TOKEN'),
            'user_id': os.getenv('MASTER_USER_ID')
        }
        
        if any(master_env.values()):
            if 'master_account' not in self.config_data:
                self.config_data['master_account'] = {}
            self.config_data['master_account'].update({k: v for k, v in master_env.items() if v})
    
    def get_kite_credentials(self) -> Optional[KiteCredentials]:
        """Get Kite credentials from configuration"""
        kite_config = self.config_data.get('kite', {})
        
        required_fields = ['user_id', 'password', 'api_key', 'api_secret', 'auth_secret', 'access_token']
        if not all(kite_config.get(field) for field in required_fields):
            logger.warning("Incomplete Kite credentials in configuration")
            return None
        
        return KiteCredentials(
            user_id=kite_config['user_id'],
            password=kite_config['password'],
            api_key=kite_config['api_key'],
            api_secret=kite_config['api_secret'],
            auth_secret=kite_config['auth_secret'],
            access_token=kite_config['access_token']
        )
    
    def get_telegram_config(self) -> Optional[TelegramConfig]:
        """Get Telegram configuration"""
        telegram_config = self.config_data.get('telegram', {})
        
        if not telegram_config.get('bot_token') or not telegram_config.get('chat_id'):
            logger.warning("Incomplete Telegram configuration")
            return None
        
        return TelegramConfig(
            bot_token=telegram_config['bot_token'],
            chat_id=telegram_config['chat_id']
        )
    
    def get_follower_configs(self) -> List[FollowerConfig]:
        """Get follower configurations"""
        followers = []
        follower_configs = self.config_data.get('followers', [])
        
        for i, config in enumerate(follower_configs):
            try:
                follower = FollowerConfig(
                    api_key=config['api_key'],
                    api_secret=config['api_secret'],
                    access_token=config['access_token'],
                    user_id=config['user_id'],
                    multiplier=config.get('multiplier', 1.0),
                    max_position_size=config.get('max_position_size', 1000),
                    enabled=config.get('enabled', True),
                    enabled_segments=config.get('enabled_segments'),
                    segment_multipliers=config.get('segment_multipliers'),
                    segment_limits=config.get('segment_limits')
                )
                followers.append(follower)
            except KeyError as e:
                logger.error(f"Invalid follower configuration {i}: missing {e}")
        
        return followers
    
    def get_system_config(self) -> SystemConfig:
        """Get system configuration"""
        system_config = self.config_data.get('system', {})
        
        return SystemConfig(
            paper_trading=system_config.get('paper_trading', True),
            log_level=system_config.get('log_level', 'INFO'),
            check_interval=system_config.get('check_interval', 1),
            max_retries=system_config.get('max_retries', 3),
            max_daily_trades=system_config.get('max_daily_trades', 100),
            risk_management_enabled=system_config.get('risk_management_enabled', True),
            auto_token_refresh=system_config.get('auto_token_refresh', True),
            market_hours_only=system_config.get('market_hours_only', True)
        )
    
    def validate_config(self) -> bool:
        """Validate the loaded configuration"""
        errors = []
        
        # Check kite credentials
        kite_creds = self.get_kite_credentials()
        if not kite_creds:
            errors.append("Missing or incomplete Kite credentials")
        
        # Check if we have either master account or followers for copy trading
        master_account = self.config_data.get('master_account', {})
        followers = self.get_follower_configs()
        
        if not master_account and not followers:
            errors.append("No master account or followers configured for copy trading")
        
        # Check enabled followers
        enabled_followers = [f for f in followers if f.enabled]
        if followers and not enabled_followers:
            errors.append("No enabled followers found")
        
        if errors:
            for error in errors:
                logger.error(f"Configuration validation error: {error}")
            return False
        
        logger.info("Configuration validation passed")
        return True
    
    def save_config(self, filename: str = None):
        """Save current configuration to file"""
        if filename is None:
            filename = self.config_file
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.config_data, f, indent=4)
            logger.info(f"Configuration saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def create_sample_config(self, filename: str = "config.json.sample"):
        """Create a sample configuration file"""
        sample_config = {
            "kite": {
                "user_id": "your_user_id_here",
                "password": "your_password_here",
                "api_key": "your_api_key_here",
                "api_secret": "your_api_secret_here",
                "auth_secret": "your_auth_secret_here",
                "access_token": "your_access_token_here"
            },
            "telegram": {
                "bot_token": "your_bot_token_here",
                "chat_id": "your_chat_id_here"
            },
            "master_account": {
                "api_key": "your_master_api_key",
                "api_secret": "your_master_api_secret",
                "access_token": "your_master_access_token",
                "user_id": "your_master_user_id"
            },
            "followers": [
                {
                    "api_key": "follower1_api_key",
                    "api_secret": "follower1_api_secret",
                    "access_token": "follower1_access_token",
                    "user_id": "follower1_user_id",
                    "multiplier": 0.5,
                    "max_position_size": 500,
                    "enabled": True
                }
            ],
            "system": {
                "paper_trading": True,
                "log_level": "INFO",
                "check_interval": 1,
                "max_retries": 3,
                "max_daily_trades": 100,
                "risk_management_enabled": True
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(sample_config, f, indent=4)
            logger.info(f"Sample configuration created: {filename}")
        except Exception as e:
            logger.error(f"Error creating sample configuration: {e}")

def main():
    """Test the configuration loader"""
    print("Testing Configuration Loader...")
    
    # Test loading configuration
    loader = ConfigLoader()
    config = loader.load_config()
    
    print(f"Loaded configuration keys: {list(config.keys())}")
    
    # Test getting specific configurations
    kite_creds = loader.get_kite_credentials()
    if kite_creds:
        print(f"Kite credentials loaded: {kite_creds.user_id}")
    else:
        print("No Kite credentials found")
    
    telegram_config = loader.get_telegram_config()
    if telegram_config:
        print(f"Telegram config loaded: {telegram_config.chat_id}")
    else:
        print("No Telegram configuration found")
    
    followers = loader.get_follower_configs()
    print(f"Found {len(followers)} follower configurations")
    
    system_config = loader.get_system_config()
    print(f"System config: paper_trading={system_config.paper_trading}")
    
    # Validate configuration
    is_valid = loader.validate_config()
    print(f"Configuration valid: {is_valid}")

if __name__ == '__main__':
    main()
