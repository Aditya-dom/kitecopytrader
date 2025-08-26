#!/usr/bin/env python3
"""
Notification Test Script
=======================

Test your notification setup before running the copy trading system.
"""

import sys
import asyncio
from datetime import datetime
from notifications import load_notification_config, NotificationManager

def test_notifications():
    """Test all configured notification channels"""
    
    print("TESTING NOTIFICATION SYSTEM")
    print("=" * 50)
    
    # Load configuration
    config = load_notification_config()
    
    # Check what's enabled
    enabled_channels = []
    if config.whatsapp_enabled:
        enabled_channels.append("WhatsApp")
    if config.telegram_enabled:
        enabled_channels.append("Telegram")
    if config.email_enabled:
        enabled_channels.append("Email")
    if config.discord_enabled:
        enabled_channels.append("Discord")
    
    if not enabled_channels:
        print("ERROR: No notification channels enabled!")
        print("\nTo enable notifications, update your .env file:")
        print("- TELEGRAM_ENABLED=True (easiest)")
        print("- WHATSAPP_ENABLED=True")
        print("- EMAIL_ENABLED=True")
        print("\nSee NOTIFICATION_SETUP.md for detailed instructions.")
        return False
    
    print(f"SUCCESS: Enabled channels: {', '.join(enabled_channels)}")
    print()
    
    # Create notification manager
    notification_manager = NotificationManager(config)
    
    # Test 1: System Alert
    print("Sending test system alert...")
    try:
        notification_manager.send_system_alert(
            "Test Alert",
            "This is a test message from your Zerodha Copy Trading System. If you receive this, notifications are working correctly!",
            "INFO"
        )
        print("SUCCESS: System alert sent")
    except Exception as e:
        print(f"ERROR: System alert failed: {e}")
    
    print()
    
    # Test 2: Sample Trade Notification
    print("Sending test trade notification...")
    try:
        sample_trade = {
            'order_id': 'TEST001',
            'tradingsymbol': 'RELIANCE',
            'exchange': 'NSE',
            'transaction_type': 'BUY',
            'quantity': 100,
            'price': 2500.50,
            'product': 'MIS',
            'order_type': 'MARKET'
        }
        
        sample_results = [
            {
                'user_id': 'FOLLOWER_TEST',
                'success': True,
                'replicated_quantity': 100,
                'error': ''
            }
        ]
        
        notification_manager.send_trade_notification(sample_trade, sample_results)
        print("SUCCESS: Trade notification sent")
    except Exception as e:
        print(f"ERROR: Trade notification failed: {e}")
    
    print()
    
    # Test 3: Daily Summary
    print("Sending test daily summary...")
    try:
        sample_summary = {
            'total_trades': 5,
            'successful_copies': 9,
            'failed_copies': 1,
            'followers': ['USER1', 'USER2'],
            'segment_breakdown': {
                'NSE': 3,
                'MCX': 1,
                'NFO': 1
            },
            'follower_performance': {
                'USER1': {'successful': 5, 'total': 5},
                'USER2': {'successful': 4, 'total': 5}
            },
            'uptime': '8:30:45'
        }
        
        notification_manager.send_daily_summary(sample_summary)
        print("SUCCESS: Daily summary sent")
    except Exception as e:
        print(f"ERROR: Daily summary failed: {e}")
    
    print()
    print("Test completed!")
    print()
    print("Check your notification channels:")
    for channel in enabled_channels:
        print(f"   - {channel}")
    print()
    print("If you didn't receive notifications:")
    print("   1. Check your .env configuration")
    print("   2. Verify credentials are correct")
    print("   3. Check NOTIFICATION_SETUP.md for help")
    
    return True

def interactive_setup():
    """Interactive notification setup"""
    print("INTERACTIVE NOTIFICATION SETUP")
    print("=" * 50)
    
    print("\nWhich notification method would you like to setup?")
    print("1. Telegram (Recommended - Free & Easy)")
    print("2. WhatsApp (via Twilio)")
    print("3. Email")
    print("4. Test existing configuration")
    print("5. Exit")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice == "1":
        setup_telegram()
    elif choice == "2":
        setup_whatsapp()
    elif choice == "3":
        setup_email()
    elif choice == "4":
        test_notifications()
    elif choice == "5":
        print("Setup cancelled")
        return
    else:
        print("Invalid choice")

def setup_telegram():
    """Guide user through Telegram setup"""
    print("\nTELEGRAM SETUP GUIDE")
    print("-" * 30)
    
    print("\n1. Open Telegram and search for @BotFather")
    print("2. Send: /newbot")
    print("3. Choose a name: My Copy Trading Bot")
    print("4. Choose username: mycopytrading_bot")
    print("5. Copy the bot token")
    
    bot_token = input("\nEnter your bot token: ").strip()
    
    print("\n6. Send a message to your bot")
    print(f"7. Visit: https://api.telegram.org/bot{bot_token}/getUpdates")
    print("8. Look for your chat ID (number in 'chat' section)")
    
    chat_id = input("Enter your chat ID: ").strip()
    
    print(f"\nSUCCESS: Add these to your .env file:")
    print(f"TELEGRAM_ENABLED=True")
    print(f"TELEGRAM_BOT_TOKEN={bot_token}")
    print(f"TELEGRAM_CHAT_ID={chat_id}")

def setup_whatsapp():
    """Guide user through WhatsApp setup"""
    print("\nWHATSAPP SETUP GUIDE")
    print("-" * 30)
    
    print("\n1. Go to https://www.twilio.com/ and create free account")
    print("2. Verify your phone number")
    print("3. Go to Console Dashboard")
    print("4. Find Account SID and Auth Token")
    
    account_sid = input("Enter Account SID: ").strip()
    auth_token = input("Enter Auth Token: ").strip()
    phone_number = input("Enter your WhatsApp number (with country code, e.g., +919876543210): ").strip()
    
    print(f"\nSUCCESS: Add these to your .env file:")
    print(f"WHATSAPP_ENABLED=True")
    print(f"TWILIO_ACCOUNT_SID={account_sid}")
    print(f"TWILIO_AUTH_TOKEN={auth_token}")
    print(f"TWILIO_WHATSAPP_FROM=whatsapp:+14155238886")
    print(f"WHATSAPP_TO=whatsapp:{phone_number}")

def setup_email():
    """Guide user through email setup"""
    print("\nEMAIL SETUP GUIDE")
    print("-" * 25)
    
    print("\n1. Enable 2-Factor Authentication on Gmail")
    print("2. Go to Google Account > Security > App passwords")
    print("3. Generate password for 'Mail'")
    print("4. Copy the 16-character password")
    
    email = input("Enter your Gmail address: ").strip()
    app_password = input("Enter your 16-character app password: ").strip()
    notify_email = input("Enter notification email (can be same): ").strip()
    
    print(f"\nSUCCESS: Add these to your .env file:")
    print(f"EMAIL_ENABLED=True")
    print(f"EMAIL_USER={email}")
    print(f"EMAIL_PASSWORD={app_password}")
    print(f"EMAIL_TO={notify_email}")

if __name__ == "__main__":
    print("ZERODHA COPY TRADING - NOTIFICATION TESTER")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        interactive_setup()
    else:
        print("\nOptions:")
        print("1. Test existing notifications: python3 test_notifications.py")
        print("2. Interactive setup: python3 test_notifications.py --setup")
        print()
        
        choice = input("Choose option (1 or 2): ").strip()
        if choice == "1":
            test_notifications()
        elif choice == "2":
            interactive_setup()
        else:
            print("Invalid choice")
