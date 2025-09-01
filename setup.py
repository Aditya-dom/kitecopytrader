#!/usr/bin/env python3
"""
Zerodha Copy Trading System Setup Script
========================================

This script helps you set up the copy trading system with proper configuration.
"""

import os
import sys
import json
import getpass
from kiteconnect import KiteConnect
from cryptography.fernet import Fernet

def print_banner():
    """Print setup banner"""
    print("=" * 70)
    print("ZERODHA COPY TRADING SYSTEM - SETUP")
    print("=" * 70)
    print()

def print_disclaimer():
    """Print safety disclaimer"""
    print("IMPORTANT DISCLAIMER:")
    print("- This system involves real money trading")
    print("- Test thoroughly with paper trading first")
    print("- You are responsible for all trades and losses")
    print()

    response = input("Do you understand and accept these risks? (y/yes/n/no): ")
    if response.lower() not in ['y', 'yes']:
        print("Setup cancelled for safety.")
        sys.exit(1)

def generate_encryption_key():
    """Generate encryption key for sensitive data"""
    key = Fernet.generate_key()
    print(f"Generated encryption key: {key.decode()}")
    print("WARNING: Save this key securely! You'll need it to decrypt your credentials.")
    return key.decode()

def get_access_token(api_key, api_secret):
    """Helper to get access token"""
    try:
        kite = KiteConnect(api_key=api_key)
        login_url = kite.login_url()

        print(f"\nPlease visit this URL to login: {login_url}")
        print("After login, copy the 'request_token' from the callback URL")

        request_token = input("Enter request_token: ").strip()

        if not request_token:
            print("ERROR: Request token is required!")
            return None

        # Generate session
        data = kite.generate_session(request_token, api_secret=api_secret)
        access_token = data["access_token"]

        # Get user profile to verify
        kite.set_access_token(access_token)
        profile = kite.profile()

        print(f"SUCCESS: Successfully authenticated: {profile['user_name']} ({profile['user_id']})")

        return {
            'access_token': access_token,
            'user_id': profile['user_id'],
            'user_name': profile['user_name']
        }

    except Exception as e:
        print(f"ERROR: Error getting access token: {e}")
        return None

def setup_master_account():
    """Setup master account configuration"""
    print("\n" + "="*50)
    print("MASTER ACCOUNT SETUP")
    print("="*50)

    api_key = input("Enter Master API Key: ").strip()
    api_secret = getpass.getpass("Enter Master API Secret: ").strip()

    if not api_key or not api_secret:
        print("ERROR: API Key and Secret are required!")
        return None

    # Get access token
    auth_data = get_access_token(api_key, api_secret)
    if not auth_data:
        return None

    return {
        'api_key': api_key,
        'api_secret': api_secret,
        'access_token': auth_data['access_token'],
        'user_id': auth_data['user_id'],
        'user_name': auth_data['user_name']
    }

def setup_follower_accounts():
    """Setup follower accounts configuration"""
    print("\n" + "="*50)
    print("FOLLOWER ACCOUNTS SETUP")
    print("="*50)

    follower_count = int(input("How many follower accounts do you want to setup? "))
    followers = []

    for i in range(follower_count):
        print(f"\n--- Follower Account {i+1} ---")

        api_key = input(f"Enter Follower {i+1} API Key: ").strip()
        api_secret = getpass.getpass(f"Enter Follower {i+1} API Secret: ").strip()

        if not api_key or not api_secret:
            print("ERROR: API Key and Secret are required!")
            continue

        # Get access token
        auth_data = get_access_token(api_key, api_secret)
        if not auth_data:
            continue

        # Get additional configuration
        multiplier = float(input(f"Enter quantity multiplier for {auth_data['user_name']} (default 1.0): ") or "1.0")
        max_position = int(input(f"Enter maximum position size for {auth_data['user_name']} (default 1000): ") or "1000")

        # Ask about segment-specific configuration
        print(f"\n--- Segment Configuration for {auth_data['user_name']} ---")
        print("Available segments: NSE, BSE, NFO (F&O), MCX (Commodity), BFO (BSE F&O), CDS (Currency)")

        segments_input = input("Enter enabled segments (comma-separated, default: all): ").strip()
        if segments_input:
            enabled_segments = [seg.strip().upper() for seg in segments_input.split(',')]
        else:
            enabled_segments = ['NSE', 'BSE', 'NFO', 'MCX', 'BFO', 'CDS']

        # Segment-specific multipliers
        segment_multipliers = {}
        segment_limits = {}

        print("\n--- Segment-Specific Settings (press Enter to use defaults) ---")
        segment_defaults = {
            'NSE': {'mult': 1.0, 'limit': 1000},
            'BSE': {'mult': 1.0, 'limit': 1000},
            'NFO': {'mult': 0.5, 'limit': 500},   # F&O: lower due to leverage
            'MCX': {'mult': 0.2, 'limit': 200},   # Commodities: much lower due to high value
            'BFO': {'mult': 0.5, 'limit': 500},   # BSE F&O
            'CDS': {'mult': 1.0, 'limit': 1000}   # Currency
        }

        for segment in enabled_segments:
            if segment in segment_defaults:
                default_mult = segment_defaults[segment]['mult']
                default_limit = segment_defaults[segment]['limit']

                mult_input = input(f"{segment} multiplier (default {default_mult}): ")
                limit_input = input(f"{segment} position limit (default {default_limit}): ")

                segment_multipliers[segment] = float(mult_input) if mult_input else default_mult
                segment_limits[segment] = int(limit_input) if limit_input else default_limit

        follower = {
            'api_key': api_key,
            'api_secret': api_secret,
            'access_token': auth_data['access_token'],
            'user_id': auth_data['user_id'],
            'user_name': auth_data['user_name'],
            'multiplier': multiplier,
            'max_position_size': max_position,
            'enabled': True,
            'enabled_segments': enabled_segments,
            'segment_multipliers': segment_multipliers,
            'segment_limits': segment_limits
        }

        followers.append(follower)
        print(f"SUCCESS: Follower account configured: {auth_data['user_name']}")

    return followers

def create_env_file(master_config, follower_configs, use_encryption=False):
    """Create .env configuration file"""

    encryption_key = None
    if use_encryption:
        encryption_key = generate_encryption_key()
        cipher = Fernet(encryption_key.encode())

        def encrypt(data):
            return cipher.encrypt(data.encode()).decode()
    else:
        def encrypt(data):
            return data

    env_content = "# Zerodha Copy Trading System Configuration\n"
    env_content += "# Generated by setup.py\n\n"

    # Master account configuration
    env_content += "# Master Account Configuration\n"
    env_content += f"MASTER_API_KEY={master_config['api_key']}\n"
    env_content += f"MASTER_API_SECRET={encrypt(master_config['api_secret'])}\n"
    env_content += f"MASTER_ACCESS_TOKEN={encrypt(master_config['access_token'])}\n"
    env_content += f"MASTER_USER_ID={master_config['user_id']}\n\n"

    # Follower accounts configuration
    env_content += "# Follower Accounts Configuration\n"
    env_content += f"FOLLOWER_COUNT={len(follower_configs)}\n\n"

    for i, follower in enumerate(follower_configs, 1):
        env_content += f"# Follower Account {i} - {follower['user_name']}\n"
        env_content += f"FOLLOWER_{i}_API_KEY={follower['api_key']}\n"
        env_content += f"FOLLOWER_{i}_API_SECRET={encrypt(follower['api_secret'])}\n"
        env_content += f"FOLLOWER_{i}_ACCESS_TOKEN={encrypt(follower['access_token'])}\n"
        env_content += f"FOLLOWER_{i}_USER_ID={follower['user_id']}\n"
        env_content += f"FOLLOWER_{i}_MULTIPLIER={follower['multiplier']}\n"
        env_content += f"FOLLOWER_{i}_MAX_POSITION={follower['max_position_size']}\n"
        env_content += f"FOLLOWER_{i}_ENABLED={follower['enabled']}\n"

        # Add segment-specific configuration
        if 'enabled_segments' in follower:
            env_content += f"FOLLOWER_{i}_ENABLED_SEGMENTS={','.join(follower['enabled_segments'])}\n"

        if 'segment_multipliers' in follower:
            for segment, multiplier in follower['segment_multipliers'].items():
                env_content += f"FOLLOWER_{i}_{segment}_MULTIPLIER={multiplier}\n"

        if 'segment_limits' in follower:
            for segment, limit in follower['segment_limits'].items():
                env_content += f"FOLLOWER_{i}_{segment}_LIMIT={limit}\n"

        env_content += "\n"

    # System configuration
    env_content += "# System Configuration\n"
    env_content += "CHECK_INTERVAL=1\n"
    env_content += "MAX_RETRIES=3\n"
    env_content += "LOG_LEVEL=INFO\n"
    env_content += "PAPER_TRADING=True\n"
    env_content += "MAX_DAILY_TRADES=100\n"
    env_content += "RISK_MANAGEMENT=True\n"

    if use_encryption:
        env_content += f"\n# Encryption Configuration\n"
        env_content += f"ENCRYPTION_KEY={encryption_key}\n"

    # Write to file
    with open('.env', 'w') as f:
        f.write(env_content)

    print(f"SUCCESS: Configuration saved to .env file")

    if use_encryption:
        print("SECURITY: Your credentials are encrypted!")
        print(f"KEY: Encryption key: {encryption_key}")
        print("WARNING: Save the encryption key securely!")

def create_gitignore():
    """Create .gitignore file to protect sensitive data"""
    gitignore_content = """# Zerodha Copy Trading System - Security Files
.env
config.json
*.log
*.key
access_tokens.json

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
"""

    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)

    print("SUCCESS: Created .gitignore to protect sensitive files")

def install_requirements():
    """Install required packages"""
    print("\n" + "="*50)
    print("INSTALLING REQUIREMENTS")
    print("="*50)

    requirements = [
        "kiteconnect==4.2.0",
        "python-dotenv==1.0.0",
        "websocket-client==1.6.4",
        "cryptography==41.0.7",
        "pydantic==2.5.0",
        "structlog==23.2.0"
    ]

    print("Installing required packages...")
    for package in requirements:
        os.system(f"pip install {package}")

    print("SUCCESS: All requirements installed successfully")

def main():
    """Main setup function"""
    print_banner()
    print_disclaimer()

    try:
        # Install requirements
        install_requirements()

        # Setup master account
        master_config = setup_master_account()
        if not master_config:
            print("ERROR: Master account setup failed!")
            sys.exit(1)

        # Setup follower accounts
        follower_configs = setup_follower_accounts()
        if not follower_configs:
            print("ERROR: No follower accounts configured!")
            sys.exit(1)

        # Ask about encryption
        use_encryption = input("\nDo you want to encrypt sensitive data? (y/n): ").lower().startswith('y')

        # Create configuration files
        create_env_file(master_config, follower_configs, use_encryption)
        create_gitignore()

        # Setup complete
        print("\n" + "="*70)
        print("SETUP COMPLETED SUCCESSFULLY!")
        print("="*70)

        print(f"SUCCESS: Master account: {master_config['user_name']} ({master_config['user_id']})")
        print(f"SUCCESS: Follower accounts: {len(follower_configs)}")

        for follower in follower_configs:
            print(f"   - {follower['user_name']} (multiplier: {follower['multiplier']})")

        print(f"SUCCESS: Paper trading mode: ENABLED (safe for testing)")
        print(f"SUCCESS: Configuration saved to: .env")
        print(f"SUCCESS: Security file created: .gitignore")

        print("\nNEXT STEPS:")
        print("1. Review the generated .env file")
        print("2. Test with paper trading first: python main.py")
        print("3. Only disable PAPER_TRADING after thorough testing")
        print("4. Monitor the system logs carefully")
        print("5. Keep your .env file secure and never commit it to git")

        print("\nREMEMBER:")
        print("- Access tokens expire daily and need to be refreshed")
        print("- Test thoroughly before using real money")
        print("- Monitor the system actively during trading")

    except KeyboardInterrupt:
        print("\nERROR: Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Setup failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
