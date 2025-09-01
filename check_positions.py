#!/usr/bin/env python3
"""
Position Checker for Zerodha Copy Trading System
===============================================

This script checks your current positions using your encrypted credentials.
"""

import os
import sys
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException
from cryptography.fernet import Fernet
import getpass
from datetime import datetime

def decrypt_credentials():
    """Decrypt your encrypted credentials"""

    # Your encrypted credentials
    encrypted_api_key = ""
    encrypted_api_secret = ""

    print("🔐 CREDENTIAL DECRYPTION")
    print("-" * 40)
    print("To decrypt your credentials, you need the encryption key")
    print("This was shown when you first set up the system")

    encryption_key = getpass.getpass("Enter encryption key: ").strip()

    if not encryption_key:
        print("❌ Encryption key is required!")
        return None, None

    try:
        cipher = Fernet(encryption_key.encode())

        api_key = cipher.decrypt(encrypted_api_key.encode()).decode()
        api_secret = cipher.decrypt(encrypted_api_secret.encode()).decode()

        print("✅ Credentials decrypted successfully")
        print(f"📋 API Key: {api_key[:10]}...")

        return api_key, api_secret

    except Exception as e:
        print(f"❌ Decryption failed: {e}")
        print("💡 Please check your encryption key")
        return None, None

def get_access_token(api_key, api_secret):
    """Generate access token for API access"""

    try:
        kite = KiteConnect(api_key=api_key)
        login_url = kite.login_url()

        print(f"\n🔑 ACCESS TOKEN GENERATION")
        print("-" * 40)
        print("Please complete the login process:")
        print(f"1. Visit: {login_url}")
        print("2. Login with your Zerodha credentials")
        print("3. Copy the 'request_token' from the callback URL")

        request_token = input("\nEnter request_token: ").strip()

        if not request_token:
            print("❌ Request token is required!")
            return None, None

        # Generate session
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]

        # Test the token
        kite.set_access_token(access_token)
        profile = kite.profile()

        print(f"✅ Access token generated successfully!")
        print(f"👤 Account: {profile['user_name']} ({profile['user_id']})")

        return kite, profile

    except Exception as e:
        print(f"❌ Access token generation failed: {e}")
        return None, None

def format_currency(amount):
    """Format currency in Indian style"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.2f}Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.2f}L"
    else:
        return f"₹{amount:,.2f}"

def display_positions(kite):
    """Display current positions"""

    print("\n" + "="*90)
    print("📊 CURRENT POSITIONS")
    print("="*90)

    try:
        positions = kite.positions()
        net_positions = positions.get('net', [])

        # Filter active positions
        active_positions = [pos for pos in net_positions if pos['quantity'] != 0]

        if not active_positions:
            print("✅ No open positions found")
            return

        print(f"{'Symbol':<18} {'Exchange':<8} {'Qty':<8} {'Avg Price':<12} {'LTP':<10} {'P&L':<12} {'Day P&L':<10}")
        print("-"*90)

        total_pnl = 0
        total_day_pnl = 0

        for pos in active_positions:
            symbol = pos['tradingsymbol'][:17]
            exchange = pos['exchange']
            qty = pos['quantity']
            avg_price = pos['average_price']
            ltp = pos['last_price']
            pnl = pos['pnl']
            day_pnl = pos['day_pnl']

            total_pnl += pnl
            total_day_pnl += day_pnl

            # Status indicators
            pnl_status = "🟢" if pnl >= 0 else "🔴"
            day_status = "🟢" if day_pnl >= 0 else "🔴"

            print(f"{symbol:<18} {exchange:<8} {qty:<8} {avg_price:<12.2f} {ltp:<10.2f} {pnl:+8.2f}{pnl_status} {day_pnl:+8.2f}{day_status}")

        print("-"*90)
        print(f"{'TOTAL':<58} {total_pnl:+12.2f} {total_day_pnl:+10.2f}")
        print(f"Active Positions: {len(active_positions)}")

        # Overall status
        if total_pnl >= 0:
            print(f"📈 Overall P&L: {format_currency(total_pnl)} (PROFIT)")
        else:
            print(f"📉 Overall P&L: {format_currency(total_pnl)} (LOSS)")

    except Exception as e:
        print(f"❌ Error fetching positions: {e}")

def display_holdings(kite):
    """Display current holdings"""

    print("\n" + "="*90)
    print("💰 CURRENT HOLDINGS")
    print("="*90)

    try:
        holdings = kite.holdings()

        if not holdings:
            print("✅ No holdings found")
            return

        print(f"{'Symbol':<18} {'Exchange':<8} {'Qty':<8} {'Avg Price':<12} {'LTP':<10} {'P&L':<12} {'Day Chg%':<8}")
        print("-"*90)

        total_investment = 0
        total_current_value = 0
        total_pnl = 0

        for holding in holdings:
            symbol = holding['tradingsymbol'][:17]
            exchange = holding['exchange']
            qty = holding['quantity']
            avg_price = holding['average_price']
            ltp = holding['last_price']
            pnl = holding['pnl']
            day_change = holding['day_change']

            investment = qty * avg_price
            current_value = qty * ltp
            day_change_pct = (day_change / ltp * 100) if ltp > 0 else 0

            total_investment += investment
            total_current_value += current_value
            total_pnl += pnl

            # Status indicators
            pnl_status = "🟢" if pnl >= 0 else "🔴"
            day_status = "🟢" if day_change >= 0 else "🔴"

            print(f"{symbol:<18} {exchange:<8} {qty:<8} {avg_price:<12.2f} {ltp:<10.2f} {pnl:+8.2f}{pnl_status} {day_change_pct:+6.2f}%{day_status}")

        print("-"*90)
        print(f"Holdings: {len(holdings)} | Investment: {format_currency(total_investment)} | Current: {format_currency(total_current_value)}")

        # Overall return
        if total_investment > 0:
            return_pct = ((total_current_value - total_investment) / total_investment) * 100
            status = "📈 GAINS" if return_pct >= 0 else "📉 LOSSES"
            print(f"Overall Return: {format_currency(total_pnl)} ({return_pct:+.2f}%) {status}")

    except Exception as e:
        print(f"❌ Error fetching holdings: {e}")

def display_margins(kite):
    """Display margin information"""

    print("\n" + "="*70)
    print("💳 MARGIN SUMMARY")
    print("="*70)

    try:
        margins = kite.margins()

        # Equity margins
        equity = margins.get('equity', {})
        if equity:
            available = equity.get('available', {})
            utilised = equity.get('utilised', {})

            cash = available.get('cash', 0)
            live_balance = available.get('live_balance', 0)
            used_margin = utilised.get('debits', 0)
            free_margin = live_balance - used_margin

            print("🔸 EQUITY SEGMENT:")
            print(f"  Available Cash: {format_currency(cash)}")
            print(f"  Total Margin: {format_currency(live_balance)}")
            print(f"  Used Margin: {format_currency(used_margin)}")
            print(f"  Free Margin: {format_currency(free_margin)}")

            # Margin utilization percentage
            if live_balance > 0:
                utilization = (used_margin / live_balance) * 100
                print(f"  Utilization: {utilization:.1f}%")

        # Commodity margins
        commodity = margins.get('commodity', {})
        if commodity:
            available = commodity.get('available', {})
            utilised = commodity.get('utilised', {})

            cash = available.get('cash', 0)
            used_margin = utilised.get('debits', 0)

            print(f"\n🔸 COMMODITY SEGMENT:")
            print(f"  Available Cash: {format_currency(cash)}")
            print(f"  Used Margin: {format_currency(used_margin)}")

    except Exception as e:
        print(f"❌ Error fetching margins: {e}")

def display_account_summary(profile):
    """Display account summary"""

    print("\n" + "="*70)
    print("👤 ACCOUNT SUMMARY")
    print("="*70)

    print(f"Name: {profile.get('user_name', 'N/A')}")
    print(f"User ID: {profile.get('user_id', 'N/A')}")
    print(f"Email: {profile.get('email', 'N/A')}")
    print(f"Mobile: {profile.get('phone', 'N/A')}")
    print(f"Broker: {profile.get('broker', 'Zerodha')}")

    # Trading segments
    segments = profile.get('products', [])
    if segments:
        print(f"Enabled Products: {', '.join(segments)}")

    exchanges = profile.get('exchanges', [])
    if exchanges:
        print(f"Enabled Exchanges: {', '.join(exchanges)}")

def main():
    """Main function to check positions"""

    print("=" * 80)
    print("🚀 ZERODHA POSITION CHECKER")
    print("=" * 80)
    print("📊 Check your current positions, holdings, and margins")
    print("🔒 Your credentials are processed securely")
    print("-" * 80)

    try:
        # Decrypt credentials
        api_key, api_secret = decrypt_credentials()
        if not api_key or not api_secret:
            sys.exit(1)

        # Get access token and connect
        kite, profile = get_access_token(api_key, api_secret)
        if not kite or not profile:
            sys.exit(1)

        # Display account information
        display_account_summary(profile)

        # Display positions
        display_positions(kite)

        # Display holdings
        display_holdings(kite)

        # Display margins
        display_margins(kite)

        print(f"\n✅ Data retrieved successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("💡 Access tokens expire daily - you'll need to regenerate tomorrow")
        print("🔄 Run this script anytime to check your current positions")

    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("💡 Common issues:")
        print("   - Wrong encryption key")
        print("   - Expired access token")
        print("   - Network connectivity")
        print("   - API rate limits")
        sys.exit(1)

if __name__ == "__main__":
    main()
