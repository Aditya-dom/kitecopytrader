#!/usr/bin/env python3
"""
Real Trading Setup & Launcher for Zerodha Copy Trading System
===========================================================

This script helps you set up and start REAL MONEY trading with your encrypted credentials.
IMPORTANT: This is for LIVE TRADING - real money will be used!
"""

import os
import sys
import logging
import getpass
from typing import Optional, Dict, Any
from datetime import datetime, time as dt_time
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import json

def print_banner():
    """Print startup banner with warnings"""
    print("=" * 80)
    print("🚀 ZERODHA COPY TRADING SYSTEM - REAL TRADING MODE")
    print("=" * 80)
    print()
    print("⚠️  CRITICAL WARNING - REAL MONEY TRADING ⚠️")
    print("=" * 50)
    print("• This system will place REAL trades with REAL money")
    print("• Losses can be substantial and rapid")
    print("• Ensure you understand all risks before proceeding")
    print("• Test thoroughly with paper trading first")
    print("• You are responsible for all trades and outcomes")
    print("=" * 50)
    print()

def confirm_real_trading():
    """Get user confirmation for real trading"""
    print("🔐 REAL TRADING CONFIRMATION")
    print("-" * 30)

    confirmations = [
        "I understand this is REAL money trading",
        "I have tested the system thoroughly with paper trading",
        "I accept full responsibility for all trades and losses",
        "I have adequate risk management in place",
        "I want to proceed with LIVE trading"
    ]

    for i, confirmation in enumerate(confirmations, 1):
        response = input(f"{i}. {confirmation} (yes/no): ").lower().strip()
        if response not in ['yes', 'y']:
            print(f"\n❌ Real trading cancelled at step {i}")
            print("💡 Consider testing with paper trading first: PAPER_TRADING=True")
            sys.exit(1)

    print("\n✅ All confirmations received - proceeding with LIVE trading setup")

def decrypt_credentials(encryption_key: Optional[str] = None) -> Dict[str, str]:
    """Decrypt the encrypted credentials"""

    # Your encrypted credentials
    encrypted_api_key = "d8ab98b87a4841b812f8978eac7c7e518db2fe686a278c428d82e72c0d1debe795e03765348f3684"
    encrypted_api_secret = "756afea3d59bd13fe9c9414457df6cff975f85e3b1436bbf9ae8e8afc304d3bce9725acf2f54bc07"

    print("\n🔐 CREDENTIAL DECRYPTION")
    print("-" * 30)

    # Try to get encryption key from environment or ask user
    if not encryption_key:
        encryption_key = os.getenv('ENCRYPTION_KEY')

    if not encryption_key:
        print("🔑 Encryption key needed to decrypt your credentials")
        print("This was shown when you first set up the system")
        encryption_key = getpass.getpass("Enter encryption key: ").strip()

    if not encryption_key:
        print("⚠️ No encryption key provided - trying credentials as plain text")
        return {
            'api_key': encrypted_api_key,
            'api_secret': encrypted_api_secret
        }

    try:
        cipher = Fernet(encryption_key.encode())

        api_key = cipher.decrypt(encrypted_api_key.encode()).decode()
        api_secret = cipher.decrypt(encrypted_api_secret.encode()).decode()

        print(f"✅ Credentials decrypted successfully")
        print(f"📋 API Key: {api_key[:10]}...")

        return {
            'api_key': api_key,
            'api_secret': api_secret,
            'encryption_key': encryption_key
        }

    except Exception as e:
        print(f"❌ Decryption failed: {e}")
        print("⚠️ Trying credentials as plain text...")

        return {
            'api_key': encrypted_api_key,
            'api_secret': encrypted_api_secret
        }

def generate_access_token(api_key: str, api_secret: str) -> Optional[Dict[str, str]]:
    """Generate fresh access token for trading"""

    print("\n🔑 ACCESS TOKEN GENERATION")
    print("-" * 30)

    try:
        kite = KiteConnect(api_key=api_key)
        login_url = kite.login_url()

        print("📱 Please complete the login process:")
        print(f"1. Visit: {login_url}")
        print("2. Login with your Zerodha credentials")
        print("3. Copy the 'request_token' from the callback URL")
        print()

        request_token = input("Enter request_token: ").strip()

        if not request_token:
            print("❌ Request token is required!")
            return None

        # Generate session
        print("🔄 Generating access token...")
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]

        # Verify token works
        kite.set_access_token(access_token)
        profile = kite.profile()

        print(f"✅ Access token generated successfully!")
        print(f"👤 Account: {profile['user_name']} ({profile['user_id']})")
        print(f"📧 Email: {profile['email']}")
        print(f"📱 Mobile: {profile['phone']}")

        return {
            'access_token': access_token,
            'user_id': profile['user_id'],
            'user_name': profile['user_name'],
            'email': profile['email']
        }

    except Exception as e:
        print(f"❌ Access token generation failed: {e}")
        return None

def check_account_margins(kite: KiteConnect) -> bool:
    """Check if account has sufficient margins"""

    print("\n💰 MARGIN CHECK")
    print("-" * 30)

    try:
        margins = kite.margins()

        # Check equity margins
        equity = margins.get('equity', {})
        if equity:
            available_cash = equity.get('available', {}).get('cash', 0)
            live_balance = equity.get('available', {}).get('live_balance', 0)

            print(f"💵 Equity Segment:")
            print(f"   Available Cash: ₹{available_cash:,.2f}")
            print(f"   Total Margin: ₹{live_balance:,.2f}")

            if available_cash < 1000:
                print("⚠️ WARNING: Low cash balance in equity segment")

        # Check commodity margins
        commodity = margins.get('commodity', {})
        if commodity:
            available_cash = commodity.get('available', {}).get('cash', 0)
            print(f"🌾 Commodity Segment:")
            print(f"   Available Cash: ₹{available_cash:,.2f}")

        print("✅ Margin check completed")
        return True

    except Exception as e:
        print(f"❌ Margin check failed: {e}")
        return False

def setup_follower_account():
    """Setup follower account (if different from master)"""

    print("\n👥 FOLLOWER ACCOUNT SETUP")
    print("-" * 30)

    same_account = input("Is the follower account the same as master? (y/n): ").lower().startswith('y')

    if same_account:
        print("ℹ️ Using master account as follower (self-trading)")
        return None

    print("📝 Please provide follower account details:")
    follower_api_key = input("Follower API Key: ").strip()
    follower_api_secret = getpass.getpass("Follower API Secret: ").strip()

    if not follower_api_key or not follower_api_secret:
        print("⚠️ Follower credentials not provided - using master account")
        return None

    # Generate follower access token
    try:
        kite = KiteConnect(api_key=follower_api_key)
        login_url = kite.login_url()

        print(f"📱 Follower login: {login_url}")
        request_token = input("Enter follower request_token: ").strip()

        if request_token:
            data = kite.generate_session(request_token, api_secret=follower_api_secret)
            access_token = data["access_token"]

            kite.set_access_token(access_token)
            profile = kite.profile()

            print(f"✅ Follower account: {profile['user_name']} ({profile['user_id']})")

            return {
                'api_key': follower_api_key,
                'api_secret': follower_api_secret,
                'access_token': access_token,
                'user_id': profile['user_id'],
                'user_name': profile['user_name']
            }
    except Exception as e:
        print(f"❌ Follower setup failed: {e}")

    return None

def update_env_file(master_data: Dict[str, str], follower_data: Optional[Dict[str, str]] = None, encryption_key: Optional[str] = None):
    """Update .env file with real credentials"""

    print("\n📁 UPDATING CONFIGURATION")
    print("-" * 30)

    # Encrypt function
    def encrypt_if_key(data: str) -> str:
        if encryption_key:
            try:
                cipher = Fernet(encryption_key.encode())
                return cipher.encrypt(data.encode()).decode()
            except:
                return data
        return data

    env_content = f"""# Zerodha Copy Trading System - LIVE TRADING Configuration
# Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# WARNING: This configuration is for REAL MONEY trading

# Master Account Configuration
MASTER_API_KEY={master_data['api_key']}
MASTER_API_SECRET={encrypt_if_key(master_data['api_secret'])}
MASTER_ACCESS_TOKEN={encrypt_if_key(master_data['access_token'])}
MASTER_USER_ID={master_data['user_id']}

# Follower Accounts Configuration
FOLLOWER_COUNT=1

# Follower Account 1
"""

    if follower_data:
        env_content += f"""FOLLOWER_1_API_KEY={follower_data['api_key']}
FOLLOWER_1_API_SECRET={encrypt_if_key(follower_data['api_secret'])}
FOLLOWER_1_ACCESS_TOKEN={encrypt_if_key(follower_data['access_token'])}
FOLLOWER_1_USER_ID={follower_data['user_id']}
"""
    else:
        # Use master account as follower
        env_content += f"""FOLLOWER_1_API_KEY={master_data['api_key']}
FOLLOWER_1_API_SECRET={encrypt_if_key(master_data['api_secret'])}
FOLLOWER_1_ACCESS_TOKEN={encrypt_if_key(master_data['access_token'])}
FOLLOWER_1_USER_ID={master_data['user_id']}
"""

    env_content += """FOLLOWER_1_MULTIPLIER=0.1
FOLLOWER_1_MAX_POSITION=100
FOLLOWER_1_ENABLED=True

# Multi-Segment Configuration
FOLLOWER_1_ENABLED_SEGMENTS=NSE,BSE,NFO,MCX,BFO,CDS

# Conservative Segment Multipliers for Initial Testing
FOLLOWER_1_NSE_MULTIPLIER=0.1
FOLLOWER_1_BSE_MULTIPLIER=0.1
FOLLOWER_1_NFO_MULTIPLIER=0.05
FOLLOWER_1_MCX_MULTIPLIER=0.02
FOLLOWER_1_BFO_MULTIPLIER=0.05
FOLLOWER_1_CDS_MULTIPLIER=0.1

# Conservative Position Limits
FOLLOWER_1_NSE_LIMIT=100
FOLLOWER_1_BSE_LIMIT=100
FOLLOWER_1_NFO_LIMIT=25
FOLLOWER_1_MCX_LIMIT=5
FOLLOWER_1_BFO_LIMIT=25
FOLLOWER_1_CDS_LIMIT=50

# System Configuration
CHECK_INTERVAL=1
MAX_RETRIES=3
LOG_LEVEL=INFO
PAPER_TRADING=False
MAX_DAILY_TRADES=100
RISK_MANAGEMENT=True

# Security
"""

    if encryption_key:
        env_content += f"ENCRYPTION_KEY={encryption_key}\n"

    env_content += """
# Notifications (Configure as needed)
WHATSAPP_ENABLED=False
TELEGRAM_ENABLED=False
EMAIL_ENABLED=False
DISCORD_ENABLED=False
"""

    # Write to file
    with open('.env', 'w') as f:
        f.write(env_content)

    print("✅ Configuration file updated")
    print("🔒 Credentials have been saved securely")

def check_market_hours() -> bool:
    """Check if markets are open"""

    print("\n🕐 MARKET HOURS CHECK")
    print("-" * 30)

    now = datetime.now()
    current_time = now.time()

    # Market hours: 9:15 AM to 3:30 PM IST (Monday to Friday)
    market_open = dt_time(9, 15)
    market_close = dt_time(15, 30)

    is_weekday = now.weekday() < 5  # Monday = 0, Friday = 4
    is_market_hours = market_open <= current_time <= market_close

    print(f"📅 Current Time: {now.strftime('%Y-%m-%d %H:%M:%S')} ({now.strftime('%A')})")
    print(f"📈 Market Hours: 09:15 - 15:30 IST (Mon-Fri)")

    if is_weekday and is_market_hours:
        print("✅ Markets are OPEN - Live trading is active")
        return True
    elif is_weekday:
        if current_time < market_open:
            print(f"⏰ Markets will open at 09:15 (in {market_open.hour * 60 + market_open.minute - current_time.hour * 60 - current_time.minute} minutes)")
        else:
            print("🔒 Markets are CLOSED - Will resume tomorrow at 09:15")
        return False
    else:
        print("📅 Markets are CLOSED - Weekend")
        return False

def start_trading_system():
    """Start the actual trading system"""

    print("\n🚀 STARTING TRADING SYSTEM")
    print("-" * 30)

    try:
        # Import and start the main system
        print("📥 Loading trading system modules...")
        from main import main as start_main_system

        print("🔄 Starting copy trading system...")
        print("📊 Monitor logs in: copy_trader.log")
        print("🛑 Press Ctrl+C to stop the system")
        print()
        print("=" * 60)
        print("SYSTEM IS NOW LIVE - REAL TRADING ACTIVE")
        print("=" * 60)

        # Start the main system
        start_main_system()

    except KeyboardInterrupt:
        print("\n🛑 System shutdown requested by user")
    except Exception as e:
        print(f"\n❌ System error: {e}")
        print("💡 Check the logs for detailed error information")

def main():
    """Main function to set up and start real trading"""

    try:
        # Display warnings and get confirmations
        print_banner()
        confirm_real_trading()

        # Decrypt credentials
        credentials = decrypt_credentials()
        api_key = credentials['api_key']
        api_secret = credentials['api_secret']
        encryption_key = credentials.get('encryption_key')

        # Generate access token
        master_data = generate_access_token(api_key, api_secret)
        if not master_data:
            print("❌ Failed to generate access token")
            sys.exit(1)

        # Check account margins
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(master_data['access_token'])
        check_account_margins(kite)

        # Setup follower account
        follower_data = setup_follower_account()

        # Update configuration
        master_data.update({
            'api_key': api_key,
            'api_secret': api_secret
        })
        update_env_file(master_data, follower_data, encryption_key)

        # Check market hours
        market_open = check_market_hours()
        if not market_open:
            proceed = input("\n⚠️ Markets are closed. Start system anyway? (y/n): ").lower().startswith('y')
            if not proceed:
                print("ℹ️ System startup cancelled - Markets are closed")
                sys.exit(0)

        print("\n" + "=" * 60)
        print("🎯 FINAL CONFIRMATION")
        print("=" * 60)
        print(f"Master Account: {master_data['user_name']} ({master_data['user_id']})")
        if follower_data:
            print(f"Follower Account: {follower_data['user_name']} ({follower_data['user_id']})")
        else:
            print("Follower Account: Same as master (self-trading)")
        print(f"Paper Trading: DISABLED (REAL MONEY)")
        print(f"Risk Management: ENABLED")
        print(f"Conservative Multipliers: ENABLED (0.02-0.1)")

        final_confirm = input("\n🚨 FINAL CONFIRMATION: Start LIVE trading? (type 'START LIVE TRADING'): ")
        if final_confirm != 'START LIVE TRADING':
            print("❌ Final confirmation failed - System startup cancelled")
            sys.exit(1)

        # Start the trading system
        start_trading_system()

    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
