#!/usr/bin/env python3
"""
Position Viewer for Zerodha Copy Trading System
==============================================

This utility helps you view your current positions and holdings
using your API credentials.
"""

import os
import sys
from typing import List, Dict, Any
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import json
from datetime import datetime

def decrypt_credential(encrypted_credential: str, encryption_key: str = None) -> str:
    """Decrypt credential if encryption key is provided"""
    if encryption_key and encrypted_credential:
        try:
            cipher = Fernet(encryption_key.encode())
            return cipher.decrypt(encrypted_credential.encode()).decode()
        except Exception as e:
            print(f"Warning: Could not decrypt credential, using as-is: {e}")
            return encrypted_credential
    return encrypted_credential

def format_currency(amount: float) -> str:
    """Format currency in Indian format"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.2f}Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.2f}L"
    else:
        return f"₹{amount:,.2f}"

def get_positions_and_holdings(api_key: str, api_secret: str, access_token: str = None):
    """Get positions and holdings from Zerodha account"""

    try:
        # Initialize KiteConnect
        kite = KiteConnect(api_key=api_key)

        # If access token is provided, use it directly
        if access_token:
            kite.set_access_token(access_token)
        else:
            # Generate access token interactively
            print("No access token provided. Generating new access token...")
            login_url = kite.login_url()
            print(f"Please visit: {login_url}")
            request_token = input("Enter request_token from callback URL: ").strip()

            if not request_token:
                print("Error: Request token is required!")
                return None

            # Generate session
            data = kite.generate_session(request_token, api_secret=api_secret)
            access_token = data["access_token"]
            kite.set_access_token(access_token)
            print(f"Generated access token: {access_token}")
            print("Save this token for future use (valid for the day)")

        # Get profile to verify connection
        profile = kite.profile()
        print(f"\n✅ Connected to account: {profile['user_name']} ({profile['user_id']})")

        # Get positions
        positions = kite.positions()

        # Get holdings
        holdings = kite.holdings()

        # Get margins
        margins = kite.margins()

        return {
            'profile': profile,
            'positions': positions,
            'holdings': holdings,
            'margins': margins
        }

    except KiteException as e:
        print(f"❌ Kite API Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def display_positions(positions_data: Dict[str, Any]):
    """Display positions in formatted table"""

    if not positions_data:
        return

    net_positions = positions_data.get('net', [])
    day_positions = positions_data.get('day', [])

    print("\n" + "="*100)
    print("📊 CURRENT POSITIONS")
    print("="*100)

    if not net_positions and not day_positions:
        print("No positions found.")
        return

    # Display net positions
    if net_positions:
        print("\n🔸 NET POSITIONS:")
        print("-"*100)
        print(f"{'Symbol':<20} {'Exchange':<8} {'Qty':<8} {'Avg Price':<12} {'LTP':<10} {'P&L':<12} {'Day P&L':<12}")
        print("-"*100)

        total_pnl = 0
        total_day_pnl = 0

        for position in net_positions:
            if position['quantity'] != 0:
                symbol = position['tradingsymbol'][:19]
                exchange = position['exchange']
                quantity = position['quantity']
                avg_price = position['average_price']
                ltp = position['last_price']
                pnl = position['pnl']
                day_pnl = position['day_pnl']

                total_pnl += pnl
                total_day_pnl += day_pnl

                # Color coding for P&L
                pnl_str = f"{pnl:+.2f}"
                day_pnl_str = f"{day_pnl:+.2f}"

                print(f"{symbol:<20} {exchange:<8} {quantity:<8} {avg_price:<12.2f} {ltp:<10.2f} {pnl_str:<12} {day_pnl_str:<12}")

        print("-"*100)
        print(f"{'TOTAL':<62} {total_pnl:+12.2f} {total_day_pnl:+12.2f}")

    # Display day positions if different
    if day_positions:
        day_with_qty = [pos for pos in day_positions if pos['quantity'] != 0]
        if day_with_qty:
            print(f"\n🔸 DAY POSITIONS: ({len(day_with_qty)} active)")
            # Similar format as net positions

def display_holdings(holdings: List[Dict[str, Any]]):
    """Display holdings in formatted table"""

    print("\n" + "="*100)
    print("💰 CURRENT HOLDINGS")
    print("="*100)

    if not holdings:
        print("No holdings found.")
        return

    print(f"{'Symbol':<20} {'Exchange':<8} {'Qty':<8} {'Avg Price':<12} {'LTP':<10} {'P&L':<12} {'Day Change':<12}")
    print("-"*100)

    total_investment = 0
    total_current_value = 0
    total_pnl = 0

    for holding in holdings:
        symbol = holding['tradingsymbol'][:19]
        exchange = holding['exchange']
        quantity = holding['quantity']
        avg_price = holding['average_price']
        ltp = holding['last_price']
        pnl = holding['pnl']
        day_change = holding['day_change']

        investment = quantity * avg_price
        current_value = quantity * ltp

        total_investment += investment
        total_current_value += current_value
        total_pnl += pnl

        day_change_pct = (day_change / ltp * 100) if ltp else 0

        print(f"{symbol:<20} {exchange:<8} {quantity:<8} {avg_price:<12.2f} {ltp:<10.2f} {pnl:+12.2f} {day_change:+8.2f}({day_change_pct:+.1f}%)")

    print("-"*100)
    print(f"Investment: {format_currency(total_investment)} | Current: {format_currency(total_current_value)} | P&L: {total_pnl:+,.2f}")

def display_margins(margins: Dict[str, Any]):
    """Display margin information"""

    print("\n" + "="*80)
    print("💳 MARGIN SUMMARY")
    print("="*80)

    equity = margins.get('equity', {})
    commodity = margins.get('commodity', {})

    if equity:
        print("\n🔸 EQUITY SEGMENT:")
        print(f"Available Cash: {format_currency(equity.get('available', {}).get('cash', 0))}")
        print(f"Opening Balance: {format_currency(equity.get('available', {}).get('opening_balance', 0))}")
        print(f"Total Margin: {format_currency(equity.get('available', {}).get('live_balance', 0))}")
        print(f"Used Margin: {format_currency(equity.get('utilised', {}).get('debits', 0))}")

    if commodity:
        print(f"\n🔸 COMMODITY SEGMENT:")
        print(f"Available Cash: {format_currency(commodity.get('available', {}).get('cash', 0))}")
        print(f"Used Margin: {format_currency(commodity.get('utilised', {}).get('debits', 0))}")

def load_credentials_from_env():
    """Load credentials from environment variables"""
    load_dotenv()

    # Try to get encryption key
    encryption_key = os.getenv('ENCRYPTION_KEY')

    # Load master account credentials
    api_key = os.getenv('MASTER_API_KEY')
    encrypted_api_secret = os.getenv('MASTER_API_SECRET')
    encrypted_access_token = os.getenv('MASTER_ACCESS_TOKEN')

    if not api_key or not encrypted_api_secret:
        return None, None, None

    # Decrypt if needed
    api_secret = decrypt_credential(encrypted_api_secret, encryption_key)
    access_token = decrypt_credential(encrypted_access_token, encryption_key) if encrypted_access_token else None

    return api_key, api_secret, access_token

def main():
    """Main function to view positions and holdings"""

    print("=" * 80)
    print("ZERODHA POSITION & HOLDINGS VIEWER")
    print("=" * 80)

    # Method 1: Try to load from .env file
    print("\n🔍 Checking for saved credentials...")
    api_key, api_secret, access_token = load_credentials_from_env()

    if api_key and api_secret:
        print(f"✅ Found credentials for API Key: {api_key[:10]}...")
        use_saved = input("Use saved credentials? (y/n): ").lower().startswith('y')

        if not use_saved:
            api_key = api_secret = access_token = None

    # Method 2: Manual input
    if not api_key or not api_secret:
        print("\n📝 Please enter your credentials manually:")
        api_key = input("Enter your API Key: ").strip()
        api_secret = input("Enter your API Secret: ").strip()
        access_token = input("Enter your Access Token (optional, press Enter to generate new): ").strip() or None

    if not api_key or not api_secret:
        print("❌ Error: API Key and Secret are required!")
        sys.exit(1)

    # Get account data
    print("\n🔄 Fetching account data...")
    account_data = get_positions_and_holdings(api_key, api_secret, access_token)

    if not account_data:
        print("❌ Failed to fetch account data!")
        sys.exit(1)

    # Display results
    display_positions(account_data['positions'])
    display_holdings(account_data['holdings'])
    display_margins(account_data['margins'])

    # Save access token for future use
    if not access_token and account_data.get('access_token'):
        save_token = input("\n💾 Save access token for future use? (y/n): ").lower().startswith('y')
        if save_token:
            # Update .env file or create new one
            env_content = f"\n# Generated Access Token ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n"
            env_content += f"MASTER_API_KEY={api_key}\n"
            env_content += f"MASTER_API_SECRET={api_secret}\n"
            env_content += f"MASTER_ACCESS_TOKEN={account_data.get('access_token', '')}\n"

            with open('.env', 'a') as f:
                f.write(env_content)
            print("✅ Credentials saved to .env file")

    print(f"\n✅ Data fetched successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💡 Tip: Access tokens expire daily. Run this script daily or use refresh_tokens.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
