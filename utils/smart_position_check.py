#!/usr/bin/env python3
"""
Smart Position Checker for Zerodha Copy Trading System
=====================================================

This script automatically detects whether your credentials are encrypted
or plain text and handles both cases.
"""

import os
import sys
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException
from cryptography.fernet import Fernet
import getpass
from datetime import datetime

def try_decrypt_credentials():
    """Try to decrypt credentials, fallback to plain text"""

    # Your credentials (could be encrypted or plain text)
    credential_api_key = ""
    credential_api_secret = ""

    print("🔐 CREDENTIAL PROCESSING")
    print("-" * 40)

    # Method 1: Try as plain text API credentials first
    print("🔍 Method 1: Testing as plain text API credentials...")
    try:
        # Check if these look like valid Zerodha API keys (they should be shorter)
        if len(credential_api_key) < 50:  # Normal API keys are ~32 chars
            print("✅ Credentials appear to be plain text")
            return credential_api_key, credential_api_secret
        else:
            print("❌ Too long to be plain text API keys - likely encrypted")
    except:
        pass

    # Method 2: Try to decrypt with user-provided key
    print("\n🔍 Method 2: Attempting decryption...")

    # Ask for encryption key (optional)
    encryption_key = getpass.getpass("Enter encryption key (or press Enter to skip): ").strip()

    if encryption_key:
        try:
            cipher = Fernet(encryption_key.encode())

            api_key = cipher.decrypt(credential_api_key.encode()).decode()
            api_secret = cipher.decrypt(credential_api_secret.encode()).decode()

            print("✅ Credentials decrypted successfully!")
            print(f"📋 API Key: {api_key[:10]}...")
            return api_key, api_secret

        except Exception as e:
            print(f"❌ Decryption failed: {e}")
    else:
        print("ℹ️ No encryption key provided, skipping decryption")

    # Method 3: Try with common encryption keys or patterns
    print("\n🔍 Method 3: Trying common patterns...")

    # Common keys that might have been used
    common_keys = [
        "zerodha_copy_trading_key",
        "kitecopytrader_key_2024",
        "copy_trading_system_key"
    ]

    for test_key in common_keys:
        try:
            # Generate Fernet key from string
            import base64
            import hashlib
            key_bytes = hashlib.sha256(test_key.encode()).digest()
            fernet_key = base64.urlsafe_b64encode(key_bytes)
            cipher = Fernet(fernet_key)

            api_key = cipher.decrypt(credential_api_key.encode()).decode()
            api_secret = cipher.decrypt(credential_api_secret.encode()).decode()

            print(f"✅ Decrypted with pattern key!")
            print(f"📋 API Key: {api_key[:10]}...")
            return api_key, api_secret

        except:
            continue

    # Method 4: Fallback - treat as plain text anyway
    print("\n🔍 Method 4: Using as plain text (fallback)")
    print("⚠️ Will attempt to use credentials as-is")
    return credential_api_key, credential_api_secret

def get_access_token(api_key, api_secret):
    """Generate access token with automatic error handling"""

    try:
        print(f"\n🔑 ACCESS TOKEN GENERATION")
        print("-" * 40)
        print(f"Testing with API Key: {api_key[:10]}...")

        kite = KiteConnect(api_key=api_key)
        login_url = kite.login_url()

        print("✅ API Key appears valid - login URL generated")
        print("\nPlease complete the login process:")
        print(f"1. Visit: {login_url}")
        print("2. Login with your Zerodha credentials")
        print("3. Copy the 'request_token' from the callback URL")

        request_token = input("\nEnter request_token: ").strip()

        if not request_token:
            print("❌ Request token is required!")
            return None, None

        # Generate session
        print("🔄 Generating access token...")
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]

        # Test the token
        kite.set_access_token(access_token)
        profile = kite.profile()

        print(f"✅ Success! Connected to account:")
        print(f"👤 Name: {profile['user_name']}")
        print(f"🆔 User ID: {profile['user_id']}")
        print(f"📧 Email: {profile.get('email', 'Not available')}")
        print(f"🔑 Access Token: {access_token}")

        return kite, profile

    except KiteException as e:
        print(f"❌ Kite API Error: {e}")
        if "Invalid API credentials" in str(e):
            print("💡 This suggests the API key/secret are incorrect")
            print("💡 They might still be encrypted or invalid")
        return None, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

def format_currency(amount):
    """Format currency in Indian style"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.2f}Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.2f}L"
    else:
        return f"₹{amount:,.2f}"

def display_quick_summary(kite):
    """Display a quick summary of positions and margins"""

    print("\n" + "="*80)
    print("📊 ACCOUNT QUICK SUMMARY")
    print("="*80)

    try:
        # Get positions
        positions = kite.positions()
        net_positions = positions.get('net', [])
        active_positions = [pos for pos in net_positions if pos['quantity'] != 0]

        # Get holdings
        holdings = kite.holdings()

        # Get margins
        margins = kite.margins()
        equity = margins.get('equity', {})
        available_cash = equity.get('available', {}).get('cash', 0)

        print(f"💰 Available Cash: {format_currency(available_cash)}")
        print(f"📊 Active Positions: {len(active_positions)}")
        print(f"💼 Holdings: {len(holdings) if holdings else 0}")

        # Calculate total P&L
        total_position_pnl = sum(pos['pnl'] for pos in active_positions)
        total_holding_pnl = sum(hold['pnl'] for hold in holdings) if holdings else 0
        total_pnl = total_position_pnl + total_holding_pnl

        if total_pnl != 0:
            pnl_status = "📈 PROFIT" if total_pnl > 0 else "📉 LOSS"
            print(f"🎯 Total P&L: {format_currency(total_pnl)} {pnl_status}")

        # Show top positions/holdings
        if active_positions:
            print(f"\n📊 Top Active Positions:")
            for pos in sorted(active_positions, key=lambda x: abs(x['pnl']), reverse=True)[:3]:
                symbol = pos['tradingsymbol'][:15]
                pnl = pos['pnl']
                pnl_indicator = "🟢" if pnl >= 0 else "🔴"
                print(f"   {symbol}: {pnl:+.2f} {pnl_indicator}")

        if holdings:
            print(f"\n💼 Top Holdings:")
            for hold in sorted(holdings, key=lambda x: abs(x['pnl']), reverse=True)[:3]:
                symbol = hold['tradingsymbol'][:15]
                pnl = hold['pnl']
                pnl_indicator = "🟢" if pnl >= 0 else "🔴"
                print(f"   {symbol}: {pnl:+.2f} {pnl_indicator}")

    except Exception as e:
        print(f"❌ Error getting summary: {e}")

def main():
    """Main function"""

    print("=" * 80)
    print("🚀 SMART ZERODHA POSITION CHECKER")
    print("=" * 80)
    print("🔍 Automatically detects encrypted vs plain text credentials")
    print("📊 Shows your positions, holdings, and account summary")
    print("-" * 80)

    try:
        # Try to get credentials (encrypted or plain)
        api_key, api_secret = try_decrypt_credentials()

        if not api_key or not api_secret:
            print("❌ Could not process credentials")
            sys.exit(1)

        # Try to connect and get access token
        kite, profile = get_access_token(api_key, api_secret)

        if not kite or not profile:
            print("\n❌ Could not connect to Zerodha API")
            print("💡 Possible issues:")
            print("   - Credentials are still encrypted and need proper decryption")
            print("   - Invalid API key/secret")
            print("   - Network connectivity issues")
            sys.exit(1)

        # Show quick summary
        display_quick_summary(kite)

        # Offer detailed view
        detailed = input(f"\n📋 Show detailed positions and holdings? (y/n): ").lower().startswith('y')

        if detailed:
            # Import detailed display functions
            from check_positions import display_positions, display_holdings, display_margins
            display_positions(kite)
            display_holdings(kite)
            display_margins(kite)

        print(f"\n✅ Data retrieved successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("💡 Save your access token for future use (valid until end of trading day)")
        print("🔄 Run this script anytime to check your positions")

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("\n🔧 TROUBLESHOOTING TIPS:")
        print("1. If credentials are encrypted, ensure you have the correct encryption key")
        print("2. Make sure your API key/secret are valid and active")
        print("3. Check your internet connection")
        print("4. Verify that your Zerodha account has API access enabled")
        sys.exit(1)

if __name__ == "__main__":
    main()
