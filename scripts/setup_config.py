#!/usr/bin/env python3
"""
Configuration Setup Script
=========================

Interactive script to help users set up their configuration files.
Supports both simple kite_config.json and complete configuration formats.

Usage:
    python scripts/setup_config.py
"""

import os
import sys
import json
import getpass
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_loader import ConfigLoader

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("ZERODHA COPY TRADING SYSTEM - CONFIGURATION SETUP")
    print("=" * 60)
    print()

def get_user_input(prompt, default="", password=False):
    """Get user input with optional default value"""
    if password:
        value = getpass.getpass(f"{prompt} (default: {default}): " if default else f"{prompt}: ")
    else:
        value = input(f"{prompt} (default: {default}): " if default else f"{prompt}: ")
    
    return value if value else default

def setup_kite_credentials():
    """Setup Kite credentials"""
    print("\n🔑 KITE CREDENTIALS SETUP")
    print("-" * 30)
    print("Enter your Zerodha Kite credentials:")
    print("(Press Enter to skip optional fields)")
    print()
    
    kite_config = {
        "user_id": get_user_input("User ID"),
        "password": get_user_input("Password", password=True),
        "api_key": get_user_input("API Key"),
        "api_secret": get_user_input("API Secret", password=True),
        "auth_secret": get_user_input("Auth Secret (for TOTP)", password=True),
        "access_token": get_user_input("Access Token (optional)", password=True)
    }
    
    return kite_config

def setup_telegram_config():
    """Setup Telegram configuration"""
    print("\n📱 TELEGRAM CONFIGURATION")
    print("-" * 30)
    print("Enter your Telegram bot credentials:")
    print("(Press Enter to skip)")
    print()
    
    telegram_config = {
        "bot_token": get_user_input("Bot Token"),
        "chat_id": get_user_input("Chat ID")
    }
    
    return telegram_config

def setup_master_account():
    """Setup master account for copy trading"""
    print("\n👑 MASTER ACCOUNT SETUP")
    print("-" * 30)
    print("Enter master account credentials for copy trading:")
    print("(Press Enter to skip)")
    print()
    
    master_config = {
        "api_key": get_user_input("Master API Key"),
        "api_secret": get_user_input("Master API Secret", password=True),
        "access_token": get_user_input("Master Access Token", password=True),
        "user_id": get_user_input("Master User ID")
    }
    
    return master_config

def setup_followers():
    """Setup follower accounts"""
    print("\n👥 FOLLOWER ACCOUNTS SETUP")
    print("-" * 30)
    
    followers = []
    follower_count = int(get_user_input("Number of follower accounts", "0") or "0")
    
    for i in range(follower_count):
        print(f"\nFollower {i+1}:")
        follower = {
            "api_key": get_user_input(f"  API Key"),
            "api_secret": get_user_input(f"  API Secret", password=True),
            "access_token": get_user_input(f"  Access Token", password=True),
            "user_id": get_user_input(f"  User ID"),
            "multiplier": float(get_user_input(f"  Multiplier (0.0-1.0)", "1.0") or "1.0"),
            "max_position_size": int(get_user_input(f"  Max Position Size", "1000") or "1000"),
            "enabled": get_user_input(f"  Enabled (y/n)", "y").lower() == 'y'
        }
        followers.append(follower)
    
    return followers

def setup_system_config():
    """Setup system configuration"""
    print("\n⚙️ SYSTEM CONFIGURATION")
    print("-" * 30)
    print("Configure system settings:")
    print()
    
    system_config = {
        "paper_trading": get_user_input("Paper Trading (y/n)", "y").lower() == 'y',
        "log_level": get_user_input("Log Level (DEBUG/INFO/WARNING/ERROR)", "INFO"),
        "check_interval": int(get_user_input("Check Interval (seconds)", "1") or "1"),
        "max_retries": int(get_user_input("Max Retries", "3") or "3"),
        "max_daily_trades": int(get_user_input("Max Daily Trades", "100") or "100"),
        "risk_management_enabled": get_user_input("Risk Management (y/n)", "y").lower() == 'y'
    }
    
    return system_config

def save_configuration(config, filename):
    """Save configuration to file"""
    try:
        with open(filename, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"✅ Configuration saved to {filename}")
        return True
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        return False

def main():
    """Main configuration setup function"""
    print_banner()
    
    print("This script will help you set up your configuration.")
    print("You can choose between a simple configuration or a complete one.")
    print()
    
    # Choose configuration type
    config_type = input("Configuration type (simple/complete): ").lower()
    if config_type not in ['simple', 'complete']:
        config_type = 'simple'
    
    print(f"\nSetting up {config_type} configuration...")
    
    # Build configuration
    config = {}
    
    # Always include kite credentials
    kite_config = setup_kite_credentials()
    config['kite'] = kite_config
    
    # Always include telegram if provided
    telegram_config = setup_telegram_config()
    if any(telegram_config.values()):
        config['telegram'] = telegram_config
    
    if config_type == 'complete':
        # Add master account
        master_config = setup_master_account()
        if any(master_config.values()):
            config['master_account'] = master_config
        
        # Add followers
        followers = setup_followers()
        if followers:
            config['followers'] = followers
        
        # Add system configuration
        system_config = setup_system_config()
        config['system'] = system_config
    
    # Choose filename
    if config_type == 'simple':
        filename = get_user_input("Configuration filename", "kite_config.json")
    else:
        filename = get_user_input("Configuration filename", "config.json")
    
    # Save configuration
    print(f"\n💾 SAVING CONFIGURATION")
    print("-" * 30)
    
    if save_configuration(config, filename):
        print(f"\n🎉 Configuration setup complete!")
        print(f"📁 Configuration saved to: {filename}")
        print()
        print("Next steps:")
        print("1. Review your configuration file")
        print("2. Test your setup: python run_tests.py --quick")
        print("3. Start trading: python run.py")
    else:
        print("\n❌ Configuration setup failed!")
        print("Please check the error messages above and try again.")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Configuration setup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
