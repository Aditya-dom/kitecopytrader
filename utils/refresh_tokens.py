#!/usr/bin/env python3
"""
Token Refresh Script for Zerodha Copy Trading System
===================================================

This script helps refresh access tokens daily.
"""

import os
import sys
from kiteconnect import KiteConnect
from dotenv import load_dotenv
import re

def refresh_tokens():
    """Refresh access tokens for all accounts"""
    load_dotenv()
    
    print("=" * 60)
    print("ZERODHA ACCESS TOKEN REFRESH")
    print("=" * 60)
    print()
    
    # Get account details from .env
    accounts = []
    
    # Master account
    master_api_key = os.getenv('MASTER_API_KEY')
    if master_api_key:
        accounts.append(('MASTER', master_api_key, os.getenv('MASTER_API_SECRET')))
    
    # Follower accounts
    follower_count = int(os.getenv('FOLLOWER_COUNT', '0'))
    for i in range(1, follower_count + 1):
        api_key = os.getenv(f'FOLLOWER_{i}_API_KEY')
        api_secret = os.getenv(f'FOLLOWER_{i}_API_SECRET')
        if api_key and api_secret:
            accounts.append((f'FOLLOWER_{i}', api_key, api_secret))
    
    if not accounts:
        print("ERROR: No accounts found in .env file")
        return False
    
    print(f"Found {len(accounts)} accounts to refresh")
    print()
    
    new_tokens = {}
    
    for account_type, api_key, api_secret in accounts:
        print(f"Refreshing {account_type}...")
        
        try:
            kite = KiteConnect(api_key=api_key)
            login_url = kite.login_url()
            
            print(f"Login URL: {login_url}")
            request_token = input(f"Enter request_token for {account_type}: ").strip()
            
            if not request_token:
                print(f"ERROR: Skipping {account_type} - no request token provided")
                continue
            
            # Generate new access token
            data = kite.generate_session(request_token, api_secret=api_secret)
            access_token = data["access_token"]
            
            # Verify token works
            kite.set_access_token(access_token)
            profile = kite.profile()
            
            print(f"SUCCESS: {account_type}: {profile['user_name']} ({profile['user_id']})")
            
            new_tokens[f'{account_type}_ACCESS_TOKEN'] = access_token
            
        except Exception as e:
            print(f"ERROR: Error refreshing {account_type}: {e}")
    
    if new_tokens:
        update_env_file(new_tokens)
        print(f"\nSUCCESS: Updated {len(new_tokens)} access tokens in .env file")
        return True
    else:
        print("\nERROR: No tokens were refreshed")
        return False

def update_env_file(new_tokens):
    """Update .env file with new access tokens"""
    
    if not os.path.exists('.env'):
        print("ERROR: .env file not found")
        return
    
    # Read current .env content
    with open('.env', 'r') as f:
        content = f.read()
    
    # Update tokens
    for token_name, token_value in new_tokens.items():
        pattern = f'{token_name}=.*'
        replacement = f'{token_name}={token_value}'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
        else:
            # Add new token if not found
            content += f'\n{replacement}\n'
    
    # Write updated content
    with open('.env', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    try:
        success = refresh_tokens()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nERROR: Token refresh cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Token refresh failed: {e}")
        sys.exit(1)
