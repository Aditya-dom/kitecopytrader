# Zerodha Copy Trading System - Setup and Use Guide

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [First Time Setup](#first-time-setup)
- [Daily Operations](#daily-operations)
- [Features Overview](#features-overview)
- [Security Guide](#security-guide)
- [Troubleshooting](#troubleshooting)
- [Advanced Configuration](#advanced-configuration)

---

## 🚀 Quick Start

### For Experienced Users
```bash
# 1. Install requirements
pip install -r requirements.txt

# 2. Run automated setup
python setup.py

# 3. Check your positions (recommended first step)
python smart_position_check.py

# 4. Start trading (after thorough testing)
python start_real_trading.py
```

### For New Users
**⚠️ READ THE FULL GUIDE BELOW BEFORE STARTING ⚠️**

---

## 💻 System Requirements

### Hardware
- **RAM**: Minimum 2GB, Recommended 4GB+
- **Storage**: 500MB free space
- **Internet**: Stable broadband connection (required for real-time trading)

### Software
- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **Browser**: For Zerodha login process

### Zerodha Account Requirements
- Active Zerodha trading account
- KiteConnect API access enabled
- Sufficient margin for trading
- Valid API credentials (API Key & Secret)

---

## 📦 Installation

### Step 1: Download and Extract
```bash
# Navigate to your desired directory
cd /Users/yourname/Desktop
# The system is already in: kitecopytrader/
```

### Step 2: Install Dependencies
```bash
cd kitecopytrader
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python -c "import kiteconnect; print('✅ Installation successful!')"
```

---

## ⚙️ Configuration

### Configuration Files Overview
- **`.env`** - Main configuration (credentials, settings)
- **`config.py`** - System configuration management
- **`.gitignore`** - Protects sensitive files from version control

### Environment Variables (.env file)
```bash
# Master Account (Your main trading account)
MASTER_API_KEY=your_api_key_here
MASTER_API_SECRET=your_api_secret_here
MASTER_ACCESS_TOKEN=your_access_token_here
MASTER_USER_ID=your_user_id_here

# Follower Account(s) - Accounts that copy trades
FOLLOWER_COUNT=1
FOLLOWER_1_API_KEY=follower_api_key
FOLLOWER_1_API_SECRET=follower_api_secret
FOLLOWER_1_ACCESS_TOKEN=follower_access_token
FOLLOWER_1_USER_ID=follower_user_id

# Risk Management
FOLLOWER_1_MULTIPLIER=0.1          # Trade 10% of master quantity
FOLLOWER_1_MAX_POSITION=100        # Maximum shares per trade
FOLLOWER_1_ENABLED=True            # Enable/disable this follower

# Trading Segments
FOLLOWER_1_ENABLED_SEGMENTS=NSE,BSE,NFO,MCX,BFO,CDS

# System Settings
PAPER_TRADING=True                 # KEEP TRUE FOR TESTING
LOG_LEVEL=INFO
RISK_MANAGEMENT=True
MAX_DAILY_TRADES=100
```

---

## 🎯 First Time Setup

### Option 1: Automated Setup (Recommended)
```bash
python setup.py
```

**This interactive script will:**
- ✅ Install all requirements
- ✅ Generate API credentials
- ✅ Create secure configuration
- ✅ Set up paper trading mode
- ✅ Configure multi-segment trading

### Option 2: Manual Setup

#### Step 1: Get API Credentials
1. Visit [KiteConnect Developer Console](https://developers.kite.trade/)
2. Create a new app
3. Note down your **API Key** and **API Secret**

#### Step 2: Generate Access Token
```python
from kiteconnect import KiteConnect

kite = KiteConnect(api_key="your_api_key")
print(kite.login_url())  # Visit this URL

# After login, get request_token from callback
data = kite.generate_session("request_token", api_secret="your_secret")
print(f"Access Token: {data['access_token']}")
```

#### Step 3: Configure Environment
```bash
cp .env.sample .env
nano .env  # Edit with your credentials
```

### Option 3: Using Encrypted Credentials
If you have encrypted credentials:
```bash
# Use the smart position checker to test
python smart_position_check.py

# Or use the dedicated encrypted credential handler
python check_positions.py
```

---

## 📊 Daily Operations

### Morning Routine (Before Market Open)

#### 1. Refresh Access Tokens (Daily Requirement)
```bash
python refresh_tokens.py
```
**Note**: Access tokens expire daily and must be refreshed

#### 2. Check Account Status
```bash
# Quick position and margin check
python smart_position_check.py

# Or detailed analysis
python check_positions.py
```

#### 3. Verify System Configuration
```bash
# Test all systems without trading
PAPER_TRADING=True python main.py
```

### During Trading Hours (9:15 AM - 3:30 PM IST)

#### Start Live Trading
```bash
# For paper trading (recommended for beginners)
PAPER_TRADING=True python main.py

# For live trading (after thorough testing)
python start_real_trading.py
```

#### Monitor Operations
- **Watch logs**: `tail -f copy_trader.log`
- **System status**: Check terminal output
- **Account monitoring**: Keep Zerodha Kite open

#### Emergency Stop
- **Graceful shutdown**: `Ctrl+C` in terminal
- **Force stop**: Close terminal/kill process
- **Disable followers**: Set `FOLLOWER_X_ENABLED=False`

### Evening Routine (After Market Close)

#### 1. Review Performance
```bash
# Check final positions
python smart_position_check.py

# Review logs
grep "TRADE" copy_trader.log | tail -20
```

#### 2. System Maintenance
```bash
# Backup logs
cp copy_trader.log logs/copy_trader_$(date +%Y%m%d).log

# Clear old logs (optional)
> copy_trader.log
```

---

## 🌟 Features Overview

### Multi-Segment Trading
- **NSE Equity**: National Stock Exchange stocks
- **BSE Equity**: Bombay Stock Exchange stocks
- **NFO**: NSE Futures & Options
- **MCX**: Commodities (Gold, Silver, Crude Oil, etc.)
- **BFO**: BSE Futures & Options
- **CDS**: Currency Derivatives

### Risk Management
- **Position Limits**: Per-segment quantity limits
- **Multipliers**: Different scaling per segment
- **Daily Limits**: Maximum trades per day
- **High-Risk Controls**: Enhanced limits for volatile instruments
- **Paper Trading**: Safe testing mode

### Notification System
- **WhatsApp**: Real-time trade alerts via Twilio
- **Telegram**: Bot-based notifications
- **Email**: Trade confirmations and summaries
- **Discord**: Team coordination webhooks

### Security Features
- **Encrypted Storage**: Credentials stored securely
- **Environment Variables**: No hardcoded secrets
- **Git Protection**: `.gitignore` prevents credential leaks
- **Access Control**: Token-based authentication

---

## 🔒 Security Guide

### Credential Protection
```bash
# ✅ DO: Use environment variables
MASTER_API_KEY=your_key

# ❌ DON'T: Hardcode in files
api_key = "your_actual_key_here"  # Never do this!
```

### File Security
```bash
# Protect sensitive files
chmod 600 .env                    # Owner read/write only
chmod 700 kitecopytrader/         # Owner access only
```

### API Security Best Practices
- **Rotate tokens**: Refresh access tokens daily
- **Monitor usage**: Check for unauthorized access
- **Limit permissions**: Use minimal required API permissions
- **Secure storage**: Never commit credentials to version control

### Network Security
- **VPN recommended**: For additional security layer
- **Firewall**: Configure appropriate rules
- **Monitoring**: Log all API interactions

---

## 🛠️ Troubleshooting

### Common Issues

#### 1. "Invalid API Credentials"
```bash
# Check credential format
echo $MASTER_API_KEY | wc -c    # Should be reasonable length

# Test credentials
python smart_position_check.py
```

#### 2. "Access Token Expired"
```bash
# Refresh tokens
python refresh_tokens.py

# Or regenerate manually
python -c "
from kiteconnect import KiteConnect
kite = KiteConnect('your_api_key')
print(kite.login_url())
"
```

#### 3. "WebSocket Connection Failed"
```bash
# Check internet connection
ping kite.zerodha.com

# Restart system
python main.py
```

#### 4. "Insufficient Funds"
```bash
# Check available margins
python smart_position_check.py

# Review position limits
grep "LIMIT" .env
```

#### 5. "Encrypted Credentials Issues"
```bash
# Try smart detection
python smart_position_check.py

# Or manual decryption
python check_positions.py
```

### Debug Mode
```bash
# Enable detailed logging
LOG_LEVEL=DEBUG python main.py

# Check specific errors
grep "ERROR" copy_trader.log
```

### Log Analysis
```bash
# Recent trades
grep "Trade replicated" copy_trader.log | tail -10

# Connection issues
grep "WebSocket" copy_trader.log

# Risk management blocks
grep "blocked by risk" copy_trader.log
```

---

## 🔧 Advanced Configuration

### Multi-Account Setup
```bash
# Multiple followers
FOLLOWER_COUNT=3

# Each with individual settings
FOLLOWER_1_MULTIPLIER=0.1
FOLLOWER_2_MULTIPLIER=0.2
FOLLOWER_3_MULTIPLIER=0.05
```

### Segment-Specific Configuration
```bash
# Different multipliers per segment
FOLLOWER_1_NSE_MULTIPLIER=0.1    # Conservative for equity
FOLLOWER_1_NFO_MULTIPLIER=0.05   # More conservative for F&O
FOLLOWER_1_MCX_MULTIPLIER=0.02   # Very conservative for commodities

# Individual limits
FOLLOWER_1_NSE_LIMIT=1000
FOLLOWER_1_NFO_LIMIT=500
FOLLOWER_1_MCX_LIMIT=100
```

### Notification Configuration
```bash
# WhatsApp via Twilio
WHATSAPP_ENABLED=True
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
WHATSAPP_TO=whatsapp:+919876543210

# Telegram
TELEGRAM_ENABLED=True
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Email
EMAIL_ENABLED=True
SMTP_SERVER=smtp.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_TO=alerts@yourdomain.com
```

### Custom Risk Rules
Modify `follower_client.py`:
```python
def custom_risk_check(self, trade_data):
    symbol = trade_data['tradingsymbol']
    
    # Block specific stocks
    blocked_stocks = ['PENNYSTK', 'RISKYSTK']
    if any(blocked in symbol for blocked in blocked_stocks):
        return False, "Stock in blocked list"
    
    # Sector limits
    if symbol.startswith('BANK'):
        max_banking_exposure = 50000  # ₹50,000
        # Custom logic here
    
    return True, "Custom check passed"
```

---

## 📈 Performance Optimization

### System Resources
```bash
# Monitor resource usage
top | grep python

# Optimize for production
# - Use SSD storage for logs
# - Dedicated network connection
# - Sufficient RAM allocation
```

### Network Optimization
```bash
# Test latency to Zerodha servers
ping kite.zerodha.com
traceroute kite.zerodha.com

# Use wired connection for stability
# Consider dedicated internet line for critical trading
```

---

## 🚨 Important Warnings

### Financial Risks
- **Capital Loss**: Trading involves substantial risk of loss
- **Leverage Risk**: F&O and commodities can amplify losses
- **System Risk**: Technical failures can result in missed trades or errors
- **Market Risk**: Rapid market movements can cause significant losses

### Technical Risks
- **Connection Loss**: Internet disruption affects real-time trading
- **API Limits**: Rate limiting can delay order execution
- **Token Expiry**: Daily token refresh required for operation
- **System Failure**: Hardware/software issues affect trading

### Regulatory Compliance
- **Broker Rules**: Follow Zerodha's terms of service
- **Tax Obligations**: Maintain records for tax reporting
- **Regulatory Changes**: Stay updated with SEBI regulations
- **Risk Disclosure**: Understand all associated risks

---

## 📞 Support and Resources

### Documentation
- **KiteConnect API**: [Official Documentation](https://kite.trade/docs/connect/v3/)
- **Zerodha Support**: [Support Portal](https://support.zerodha.com/)

### System Files
- **Main System**: `main.py` - Core trading system
- **Configuration**: `config.py` - Settings management
- **Master Client**: `master_client.py` - Trade monitoring
- **Follower Client**: `follower_client.py` - Trade replication
- **Notifications**: `notifications.py` - Alert system

### Utility Scripts
- **Setup**: `setup.py` - Interactive system setup
- **Position Check**: `smart_position_check.py` - Account status
- **Token Refresh**: `refresh_tokens.py` - Daily token update
- **Real Trading**: `start_real_trading.py` - Live trading launcher

### Log Files
- **Main Log**: `copy_trader.log` - System operations
- **Error Log**: Errors are logged with full details
- **Trade Log**: All trade activities recorded

---

## 🎯 Best Practices

### Trading
1. **Start Small**: Begin with minimal quantities and conservative multipliers
2. **Test Thoroughly**: Use paper trading extensively before live trading
3. **Monitor Actively**: Watch the system during market hours
4. **Risk Management**: Never trade more than you can afford to lose
5. **Regular Reviews**: Analyze performance and adjust settings

### System Management
1. **Daily Maintenance**: Refresh tokens, check logs, verify balances
2. **Backup Strategy**: Regular backups of configuration and logs
3. **Security Updates**: Keep system and dependencies updated
4. **Network Monitoring**: Ensure stable internet connection
5. **Emergency Procedures**: Have manual trading backup plans

### Development
1. **Version Control**: Use git for configuration management (exclude .env)
2. **Testing Environment**: Maintain separate test configuration
3. **Code Review**: Review any custom modifications carefully
4. **Documentation**: Document any changes or customizations
5. **Rollback Plan**: Ability to revert to previous working configuration

---

## 📜 License and Disclaimer

This software is provided for educational and personal use. Users are responsible for:
- Understanding all associated risks
- Complying with applicable regulations
- Ensuring proper testing before live use
- Maintaining secure handling of credentials
- All trading decisions and their outcomes

**USE AT YOUR OWN RISK. NO WARRANTY PROVIDED.**

---

*Last Updated: 2024*
*Version: 1.0*