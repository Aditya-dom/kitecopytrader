#!/usr/bin/env python3
"""
Simple Position Viewer for Zerodha Account
==========================================

This script allows you to view positions using plain API credentials.
Enter your API key and secret directly.
"""

from kiteconnect import KiteConnect
import sys

def format_currency(amount: float) -> str:
    """Format currency in Indian format"""
    if amount >= 10000000:  # 1 crore
        return f"₹{amount/10000000:.2f}Cr"
    elif amount >= 100000:  # 1 lakh
        return f"₹{amount/100000:.2f}L"
    else:
        return f"₹{amount:,.2f}"

def view_positions():
    """View positions with plain credentials"""

    print("Enter your Zerodha API credentials:")
    api_key = input("API Key: ").strip()
    api_secret = input("API Secret: ").strip()

    if not api_key or not api_secret:
        print("❌ Error: Both API Key and Secret are required!")
        return

    # Optional: use existing access token
    access_token = input("Access Token (optional, press Enter to generate new): ").strip()

    try:
        kite = KiteConnect(api_key=api_key)

        if not access_token:
            # Generate new access token
            login_url = kite.login_url()
            print(f"\nPlease visit: {login_url}")
            print("After login, copy the 'request_token' from the URL")

            request_token = input("Enter request_token: ").strip()
            if not request_token:
                print("❌ Error: Request token is required!")
                return

            # Generate session
            data = kite.generate_session(request_token, api_secret=api_secret)
            access_token = data["access_token"]
            print(f"\n✅ Generated access token: {access_token}")

        kite.set_access_token(access_token)

        # Get profile
        profile = kite.profile()
        print(f"\n🎯 Account: {profile['user_name']} ({profile['user_id']})")

        # Get positions
        print("\n" + "="*90)
        print("📊 CURRENT POSITIONS")
        print("="*90)

        positions = kite.positions()
        net_positions = positions.get('net', [])

        active_positions = [pos for pos in net_positions if pos['quantity'] != 0]

        if not active_positions:
            print("✅ No open positions found.")
        else:
            print(f"{'Symbol':<20} {'Exchange':<8} {'Qty':<8} {'Avg Price':<12} {'LTP':<10} {'P&L':<12} {'Day P&L':<12}")
            print("-"*90)

            total_pnl = 0
            total_day_pnl = 0

            for pos in active_positions:
                symbol = pos['tradingsymbol'][:19]
                exchange = pos['exchange']
                qty = pos['quantity']
                avg_price = pos['average_price']
                ltp = pos['last_price']
                pnl = pos['pnl']
                day_pnl = pos['day_pnl']

                total_pnl += pnl
                total_day_pnl += day_pnl

                # Color indicators
                pnl_indicator = "🟢" if pnl >= 0 else "🔴"
                day_pnl_indicator = "🟢" if day_pnl >= 0 else "🔴"

                print(f"{symbol:<20} {exchange:<8} {qty:<8} {avg_price:<12.2f} {ltp:<10.2f} {pnl:+12.2f}{pnl_indicator} {day_pnl:+12.2f}{day_pnl_indicator}")

            print("-"*90)
            print(f"{'TOTAL':<60} {total_pnl:+12.2f} {total_day_pnl:+12.2f}")
            print(f"Active Positions: {len(active_positions)}")

        # Get holdings
        print("\n" + "="*90)
        print("💰 CURRENT HOLDINGS")
        print("="*90)

        holdings = kite.holdings()

        if not holdings:
            print("✅ No holdings found.")
        else:
            print(f"{'Symbol':<20} {'Exchange':<8} {'Qty':<8} {'Avg Price':<12} {'LTP':<10} {'P&L':<12} {'Day Chg%':<10}")
            print("-"*90)

            total_investment = 0
            total_current_value = 0
            total_holding_pnl = 0

            for holding in holdings:
                symbol = holding['tradingsymbol'][:19]
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
                total_holding_pnl += pnl

                # Color indicators
                pnl_indicator = "🟢" if pnl >= 0 else "🔴"
                day_indicator = "🟢" if day_change >= 0 else "🔴"

                print(f"{symbol:<20} {exchange:<8} {qty:<8} {avg_price:<12.2f} {ltp:<10.2f} {pnl:+12.2f}{pnl_indicator} {day_change_pct:+8.2f}%{day_indicator}")

            print("-"*90)
            print(f"Total Holdings: {len(holdings)}")
            print(f"Investment: {format_currency(total_investment)}")
            print(f"Current Value: {format_currency(total_current_value)}")
            print(f"Overall P&L: {format_currency(total_holding_pnl)} ({((total_current_value - total_investment) / total_investment * 100):+.2f}%)")

        # Get margins
        print("\n" + "="*70)
        print("💳 MARGIN SUMMARY")
        print("="*70)

        margins = kite.margins()

        # Equity segment
        equity = margins.get('equity', {})
        if equity:
            available = equity.get('available', {})
            utilised = equity.get('utilised', {})

            cash = available.get('cash', 0)
            live_balance = available.get('live_balance', 0)
            used_margin = utilised.get('debits', 0)

            print("\n🔸 EQUITY SEGMENT:")
            print(f"  💰 Available Cash: {format_currency(cash)}")
            print(f"  📊 Total Margin Available: {format_currency(live_balance)}")
            print(f"  📉 Used Margin: {format_currency(used_margin)}")
            print(f"  📈 Free Margin: {format_currency(live_balance - used_margin)}")

        # Commodity segment
        commodity = margins.get('commodity', {})
        if commodity:
            available = commodity.get('available', {})
            utilised = commodity.get('utilised', {})

            cash = available.get('cash', 0)
            used_margin = utilised.get('debits', 0)

            print(f"\n🔸 COMMODITY SEGMENT:")
            print(f"  💰 Available Cash: {format_currency(cash)}")
            print(f"  📉 Used Margin: {format_currency(used_margin)}")

        # Summary
        print("\n" + "="*70)
        print("📋 ACCOUNT SUMMARY")
        print("="*70)
        print(f"👤 Account Holder: {profile.get('user_name', 'N/A')}")
        print(f"🆔 User ID: {profile.get('user_id', 'N/A')}")
        print(f"📧 Email: {profile.get('email', 'N/A')}")
        print(f"📱 Mobile: {profile.get('phone', 'N/A')}")
        print(f"🏢 Broker: {profile.get('broker', 'N/A')}")

        if active_positions:
            print(f"📊 Active Positions: {len(active_positions)} (P&L: {format_currency(total_pnl)})")
        if holdings:
            print(f"💰 Holdings: {len(holdings)} (P&L: {format_currency(total_holding_pnl)})")

        overall_pnl = total_pnl + total_holding_pnl
        if overall_pnl != 0:
            status = "🟢 PROFIT" if overall_pnl > 0 else "🔴 LOSS"
            print(f"🎯 Overall P&L: {format_currency(overall_pnl)} {status}")

        print(f"\n✅ Data retrieved successfully!")
        print(f"🔑 Your access token (valid today): {access_token}")
        print("💡 Save this token to avoid re-authentication today")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Common issues:")
        print("   - Invalid API credentials")
        print("   - Expired access token")
        print("   - Network connectivity issues")
        print("   - API rate limits")

def main():
    """Main function"""
    print("=" * 70)
    print("🚀 ZERODHA POSITION & HOLDINGS VIEWER")
    print("=" * 70)
    print("\n📝 This tool helps you view your current positions and holdings")
    print("🔒 Your credentials are not stored anywhere")
    print("⚡ Access tokens are valid for the trading day only")
    print("\n" + "-" * 70)

    try:
        view_positions()
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
