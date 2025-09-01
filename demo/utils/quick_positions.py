#!/usr/bin/env python3
"""
Quick Position Checker for Zerodha Account
==========================================

This script quickly checks your positions using your encrypted credentials.
"""

from kiteconnect import KiteConnect
from cryptography.fernet import Fernet
import sys

def decrypt_credential(encrypted_credential: str, encryption_key: str) -> str:
    """Decrypt the encrypted credential"""
    try:
        cipher = Fernet(encryption_key.encode())
        return cipher.decrypt(encrypted_credential.encode()).decode()
    except Exception as e:
        print(f"Error decrypting credential: {e}")
        return None

def check_positions():
    """Check positions with your encrypted credentials"""

    # Your encrypted credentials
    encrypted_api_key = "d8ab98b87a4841b812f8978eac7c7e518db2fe686a278c428d82e72c0d1debe795e03765348f3684"
    encrypted_api_secret = "756afea3d59bd13fe9c9414457df6cff975f85e3b1436bbf9ae8e8afc304d3bce9725acf2f54bc07"

    # You need to provide the encryption key
    print("To decrypt your credentials, you need the encryption key.")
    print("This was shown when you first set up the system.")
    encryption_key = input("Enter your encryption key: ").strip()

    if not encryption_key:
        print("Error: Encryption key is required!")
        return

    # Decrypt credentials
    print("Decrypting credentials...")
    api_key = decrypt_credential(encrypted_api_key, encryption_key)
    api_secret = decrypt_credential(encrypted_api_secret, encryption_key)

    if not api_key or not api_secret:
        print("Error: Could not decrypt credentials. Please check your encryption key.")
        return

    print(f"✅ Credentials decrypted successfully")
    print(f"API Key: {api_key[:10]}...")

    # Generate access token
    try:
        kite = KiteConnect(api_key=api_key)
        login_url = kite.login_url()

        print(f"\nPlease visit this URL to login: {login_url}")
        print("After login, copy the 'request_token' from the callback URL")

        request_token = input("Enter request_token: ").strip()

        if not request_token:
            print("Error: Request token is required!")
            return

        # Generate session
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]
        kite.set_access_token(access_token)

        # Get profile
        profile = kite.profile()
        print(f"\n✅ Connected to: {profile['user_name']} ({profile['user_id']})")

        # Get positions
        print("\n" + "="*80)
        print("📊 CURRENT POSITIONS")
        print("="*80)

        positions = kite.positions()
        net_positions = positions.get('net', [])

        if not net_positions:
            print("No positions found.")
        else:
            print(f"{'Symbol':<15} {'Exchange':<8} {'Qty':<8} {'Avg Price':<12} {'LTP':<10} {'P&L':<12}")
            print("-"*75)

            total_pnl = 0
            active_positions = 0

            for position in net_positions:
                if position['quantity'] != 0:
                    active_positions += 1
                    symbol = position['tradingsymbol'][:14]
                    exchange = position['exchange']
                    quantity = position['quantity']
                    avg_price = position['average_price']
                    ltp = position['last_price']
                    pnl = position['pnl']

                    total_pnl += pnl

                    print(f"{symbol:<15} {exchange:<8} {quantity:<8} {avg_price:<12.2f} {ltp:<10.2f} {pnl:+12.2f}")

            print("-"*75)
            print(f"Total Active Positions: {active_positions}")
            print(f"Total P&L: ₹{total_pnl:+,.2f}")

        # Get holdings
        print("\n" + "="*80)
        print("💰 CURRENT HOLDINGS")
        print("="*80)

        holdings = kite.holdings()

        if not holdings:
            print("No holdings found.")
        else:
            print(f"{'Symbol':<15} {'Exchange':<8} {'Qty':<8} {'Avg Price':<12} {'LTP':<10} {'P&L':<12}")
            print("-"*75)

            total_investment = 0
            total_current_value = 0
            total_holding_pnl = 0

            for holding in holdings:
                symbol = holding['tradingsymbol'][:14]
                exchange = holding['exchange']
                quantity = holding['quantity']
                avg_price = holding['average_price']
                ltp = holding['last_price']
                pnl = holding['pnl']

                investment = quantity * avg_price
                current_value = quantity * ltp

                total_investment += investment
                total_current_value += current_value
                total_holding_pnl += pnl

                print(f"{symbol:<15} {exchange:<8} {quantity:<8} {avg_price:<12.2f} {ltp:<10.2f} {pnl:+12.2f}")

            print("-"*75)
            print(f"Total Holdings: {len(holdings)}")
            print(f"Investment: ₹{total_investment:,.2f}")
            print(f"Current Value: ₹{total_current_value:,.2f}")
            print(f"Total P&L: ₹{total_holding_pnl:+,.2f}")

        # Get margins
        print("\n" + "="*80)
        print("💳 AVAILABLE MARGINS")
        print("="*80)

        margins = kite.margins()

        equity = margins.get('equity', {})
        if equity:
            available_cash = equity.get('available', {}).get('cash', 0)
            live_balance = equity.get('available', {}).get('live_balance', 0)
            used_margin = equity.get('utilised', {}).get('debits', 0)

            print(f"Equity Segment:")
            print(f"  Available Cash: ₹{available_cash:,.2f}")
            print(f"  Live Balance: ₹{live_balance:,.2f}")
            print(f"  Used Margin: ₹{used_margin:,.2f}")

        commodity = margins.get('commodity', {})
        if commodity:
            available_cash = commodity.get('available', {}).get('cash', 0)
            used_margin = commodity.get('utilised', {}).get('debits', 0)

            print(f"Commodity Segment:")
            print(f"  Available Cash: ₹{available_cash:,.2f}")
            print(f"  Used Margin: ₹{used_margin:,.2f}")

        print(f"\n✅ Data retrieved successfully!")
        print(f"💡 Your access token for today: {access_token}")
        print("Save this token to avoid re-authentication today.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("QUICK POSITION CHECKER FOR ZERODHA ACCOUNT")
    print("=" * 80)

    try:
        check_positions()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
