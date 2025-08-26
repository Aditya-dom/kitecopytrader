#!/usr/bin/env python3
"""
Multi-Segment Trading Example for Zerodha Copy Trading System
============================================================

This example demonstrates how the system handles different trading segments:
- NSE/BSE Equity
- NFO/BFO F&O (Futures & Options)
- MCX Commodities
- CDS Currency Derivatives

Run this to see sample trade processing across all segments.
"""

import logging
from datetime import datetime

# Setup logging to see the multi-segment processing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample trades from different segments
sample_trades = [
    {
        'order_id': 'NSE001',
        'tradingsymbol': 'RELIANCE',
        'exchange': 'NSE',
        'transaction_type': 'BUY',
        'quantity': 100,
        'price': 2500.50,
        'product': 'MIS',
        'order_type': 'MARKET',
        'timestamp': datetime.now(),
        'user_id': 'MASTER123'
    },
    {
        'order_id': 'MCX001', 
        'tradingsymbol': 'GOLD24DECFUT',
        'exchange': 'MCX',
        'transaction_type': 'BUY',
        'quantity': 1,
        'price': 62000.0,
        'product': 'NRML',
        'order_type': 'MARKET',
        'timestamp': datetime.now(),
        'user_id': 'MASTER123'
    },
    {
        'order_id': 'NFO001',
        'tradingsymbol': 'NIFTY24DEC21000CE',
        'exchange': 'NFO',
        'transaction_type': 'BUY', 
        'quantity': 50,
        'price': 125.50,
        'product': 'MIS',
        'order_type': 'LIMIT',
        'timestamp': datetime.now(),
        'user_id': 'MASTER123'
    },
    {
        'order_id': 'CDS001',
        'tradingsymbol': 'USDINR24DECFUT',
        'exchange': 'CDS',
        'transaction_type': 'SELL',
        'quantity': 1,
        'price': 84.25,
        'product': 'MIS',
        'order_type': 'MARKET',
        'timestamp': datetime.now(),
        'user_id': 'MASTER123'
    },
    {
        'order_id': 'BSE001',
        'tradingsymbol': 'SENSEX',
        'exchange': 'BSE',
        'transaction_type': 'BUY',
        'quantity': 10,
        'price': 500.75,
        'product': 'CNC',
        'order_type': 'MARKET',
        'timestamp': datetime.now(),
        'user_id': 'MASTER123'
    }
]

def demonstrate_multi_segment_processing():
    """Demonstrate how trades are processed across different segments"""
    
    print("=" * 80)
    print("ZERODHA MULTI-SEGMENT COPY TRADING DEMONSTRATION")
    print("=" * 80)
    print()
    
    print("SUPPORTED TRADING SEGMENTS:")
    print("SUCCESS: NSE - National Stock Exchange (Equities)")
    print("SUCCESS: BSE - Bombay Stock Exchange (Equities)")
    print("SUCCESS: NFO - NSE Futures & Options")
    print("SUCCESS: MCX - Multi Commodity Exchange")
    print("SUCCESS: BFO - BSE Futures & Options")
    print("SUCCESS: CDS - Currency Derivatives Segment")
    print()
    
    print("SEGMENT-SPECIFIC RISK MANAGEMENT:")
    print("• NSE/BSE Equity: Standard position limits")
    print("• NFO/BFO F&O: Reduced limits due to leverage")
    print("• MCX Commodities: Much smaller limits due to high value")
    print("• CDS Currency: Standard limits with currency-specific controls")
    print()
    
    print("PROCESSING SAMPLE TRADES:")
    print("-" * 50)
    
    for i, trade in enumerate(sample_trades, 1):
        exchange = trade['exchange']
        symbol = trade['tradingsymbol']
        quantity = trade['quantity']
        transaction = trade['transaction_type']
        
        print(f"\n{i}. {exchange} Trade: {symbol}")
        print(f"   Action: {transaction} {quantity} shares/lots")
        print(f"   Price: ₹{trade['price']}")
        
        # Simulate segment-specific processing
        if exchange == 'NSE':
            print("   NSE Equity - Full multiplier applied")
            print("   Standard position limits")
            
        elif exchange == 'BSE':
            print("   BSE Equity - Full multiplier applied")
            print("   Standard position limits")
            
        elif exchange == 'NFO':
            if 'CE' in symbol or 'PE' in symbol:
                print("   NSE Options - Enhanced risk management")
                print("   50% multiplier due to leverage")
                print("   Options-specific position limits")
            else:
                print("   NSE Futures - Reduced multiplier")
                print("   50% multiplier due to leverage")
                
        elif exchange == 'MCX':
            print("   Commodity Trading - High-value asset")
            print("   20% multiplier (much lower due to high value)")
            print("   Strict position limits")
            
            # Commodity-specific risk checks
            high_risk_commodities = ['GOLD', 'SILVER', 'CRUDEOIL', 'NATURALGAS']
            if any(commodity in symbol for commodity in high_risk_commodities):
                print("   WARNING: High-risk commodity detected - Additional limits applied")
                
        elif exchange == 'BFO':
            print("   BSE F&O - Reduced multiplier")
            print("   50% multiplier due to leverage")
            
        elif exchange == 'CDS':
            print("   Currency Derivative - Standard processing")
            print("   Full multiplier for currency trades")
            
        print(f"   SUCCESS: Trade validated and ready for replication")
    
    print("\n" + "="*80)
    print("FOLLOWER ACCOUNT REPLICATION SIMULATION")
    print("="*80)
    
    # Simulate follower configurations
    follower_configs = [
        {
            'name': 'Conservative Follower',
            'segments': ['NSE', 'BSE', 'CDS'],  # Only equity and currency
            'multipliers': {'NSE': 0.5, 'BSE': 0.5, 'CDS': 0.5},
            'limits': {'NSE': 500, 'BSE': 500, 'CDS': 500}
        },
        {
            'name': 'Aggressive Follower', 
            'segments': ['NSE', 'BSE', 'NFO', 'MCX', 'CDS'],  # Most segments
            'multipliers': {'NSE': 1.0, 'BSE': 1.0, 'NFO': 0.3, 'MCX': 0.1, 'CDS': 1.0},
            'limits': {'NSE': 1000, 'BSE': 1000, 'NFO': 300, 'MCX': 100, 'CDS': 1000}
        },
        {
            'name': 'Commodity Specialist',
            'segments': ['MCX', 'CDS'],  # Only commodities and currency
            'multipliers': {'MCX': 0.5, 'CDS': 1.0},
            'limits': {'MCX': 500, 'CDS': 1000}
        }
    ]
    
    for follower in follower_configs:
        print(f"\n{follower['name']}:")
        print(f"   Enabled Segments: {', '.join(follower['segments'])}")
        
        for trade in sample_trades:
            exchange = trade['exchange']
            symbol = trade['tradingsymbol']
            original_qty = trade['quantity']
            
            if exchange in follower['segments']:
                multiplier = follower['multipliers'].get(exchange, 0)
                limit = follower['limits'].get(exchange, 0)
                adjusted_qty = int(original_qty * multiplier)
                
                if adjusted_qty <= limit:
                    print(f"   SUCCESS: {exchange} {symbol}: {original_qty} → {adjusted_qty} (Within limits)")
                else:
                    print(f"   WARNING: {exchange} {symbol}: {original_qty} → BLOCKED (Exceeds limit of {limit})")
            else:
                print(f"   SEGMENT DISABLED: {exchange} {symbol}")
    
    print("\n" + "="*80)
    print("KEY ADVANTAGES OF MULTI-SEGMENT SUPPORT")
    print("="*80)
    print("SUCCESS: Complete market coverage across all major Indian exchanges")
    print("SUCCESS: Segment-specific risk management and position sizing")
    print("SUCCESS: Flexible follower configurations per trading style")
    print("SUCCESS: Enhanced risk controls for high-leverage instruments")
    print("SUCCESS: Commodity trading with appropriate position limits")
    print("SUCCESS: Currency derivatives support for forex exposure")
    print("SUCCESS: Individual segment enable/disable per follower")
    print("SUCCESS: Granular multiplier control per segment")
    
    print("\nCONFIGURATION TIPS:")
    print("• Use lower multipliers for F&O due to leverage")
    print("• Set strict limits for commodities due to high value")
    print("• Enable only familiar segments for each follower")
    print("• Test with paper trading across all segments first")
    print("• Monitor margin requirements for each segment")
    
    print("\nREMEMBER:")
    print("• Different segments have different margin requirements")
    print("• F&O and commodities carry higher risk due to leverage")
    print("• Always test with paper trading first")
    print("• Ensure adequate margins in all follower accounts")
    print("• Monitor positions across all segments actively")

if __name__ == "__main__":
    demonstrate_multi_segment_processing()
