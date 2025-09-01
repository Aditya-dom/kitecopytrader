# Zerodha Copy Trading System - Project Structure

## 📁 Main Directory Structure

```
kitecopytrader/
├── 📄 Setup_and_Use.md          # Complete setup and usage guide
├── 📄 README.md                 # Project overview and quick start
├── 📄 PROJECT_STRUCTURE.md      # This file - project organization
├── 📄 NOTIFICATION_SETUP.md     # Notification system setup guide
├── 📄 requirements.txt          # Python dependencies
├── 📄 .gitignore               # Git security - protects sensitive files
├── 📄 .env                     # Main configuration (NOT in git)
├── 📂 demo/                    # Examples, tests, and utilities
└── 📂 core system files...
```

## 🎯 Core System Files

### Main Application
- **`main.py`** - Central orchestrator and system launcher
- **`config.py`** - Configuration management and security
- **`master_client.py`** - WebSocket monitoring of master account
- **`follower_client.py`** - Trade replication for follower accounts
- **`notifications.py`** - Multi-channel notification system

### Setup and Utilities
- **`setup.py`** - Interactive system setup wizard
- **`refresh_tokens.py`** - Daily access token refresh utility
- **`smart_position_check.py`** - Smart credential detection and position viewer
- **`check_positions.py`** - Position checker for encrypted credentials
- **`start_real_trading.py`** - Live trading launcher with safety checks

## 📂 Demo Directory

```
demo/
├── 📄 README.md                    # Demo documentation
├── 📄 multi_segment_example.py     # Multi-segment trading demonstration
├── 📄 test_notifications.py        # Notification system testing
├── 📄 cleanup.py                   # System cleanup utility
├── 📄 start.sh                     # Demo startup script
├── 📄 .env.test                    # Test environment configuration
├── 📄 CLEANUP_COMPLETE.txt         # Cleanup status
├── 📄 readme-documentation-backup.md # Backup documentation
└── 📂 utils/                       # Utility scripts
    ├── 📄 position_viewer.py        # Detailed position analysis
    ├── 📄 quick_positions.py        # Quick position checker
    └── 📄 simple_positions.py       # Simple position viewer
```

## 🔧 File Categories

### 🚀 **Production Ready Files**
Files you use for actual trading:
- `main.py` - Start the copy trading system
- `setup.py` - First-time system setup
- `start_real_trading.py` - Live trading with safety checks
- `smart_position_check.py` - Check positions and test credentials
- `refresh_tokens.py` - Daily token maintenance

### ⚙️ **Configuration Files**
- `.env` - Your credentials and settings (NEVER commit to git)
- `config.py` - Configuration management code
- `requirements.txt` - Python package dependencies
- `.gitignore` - Protects your sensitive files

### 📚 **Documentation Files**
- `Setup_and_Use.md` - **START HERE** - Complete setup guide
- `README.md` - Project overview and features
- `PROJECT_STRUCTURE.md` - This file
- `NOTIFICATION_SETUP.md` - Notification configuration help

### 🧪 **Demo and Testing Files**
All in `demo/` folder:
- Examples and demonstrations
- Testing utilities
- Development tools
- Backup configurations

## 🎯 Usage Workflow

### 1. **First Time Setup**
```bash
# Read the documentation first
cat Setup_and_Use.md

# Run interactive setup
python setup.py
```

### 2. **Daily Trading Routine**
```bash
# Morning: Refresh tokens
python refresh_tokens.py

# Check account status
python smart_position_check.py

# Start trading (paper mode first!)
python main.py

# Or for live trading (after thorough testing)
python start_real_trading.py
```

### 3. **Monitoring and Maintenance**
```bash
# Check logs
tail -f copy_trader.log

# Emergency stop
Ctrl+C in the terminal running main.py
```

## 🛡️ Security Architecture

### Protected Files
- `.env` - Contains API credentials (encrypted or plain)
- `copy_trader.log` - Trading activity logs
- `*.key` - Any encryption key files
- `config.json` - If created, contains account settings

### Public Files
- All `.py` files (code only, no credentials)
- Documentation files (`.md`)
- `requirements.txt`
- `.gitignore`

### Git Protection
The `.gitignore` file automatically protects:
```
.env
*.log
*.key
config.json
access_tokens.json
```

## 📊 System Components

### Real-Time Trading Engine
- **WebSocket Client**: Monitors master account trades
- **Event Processing**: Validates and processes trade events
- **Risk Management**: Applies position limits and safety checks
- **Order Execution**: Places trades on follower accounts

### Multi-Segment Support
- **NSE**: National Stock Exchange (Equity)
- **BSE**: Bombay Stock Exchange (Equity)
- **NFO**: NSE Futures & Options
- **MCX**: Multi Commodity Exchange
- **BFO**: BSE Futures & Options
- **CDS**: Currency Derivatives Segment

### Notification System
- **WhatsApp**: Via Twilio API
- **Telegram**: Bot integration
- **Email**: SMTP notifications
- **Discord**: Webhook alerts

## 🔍 File Dependencies

### Core Dependencies
```
main.py
├── config.py (configuration)
├── master_client.py (trade monitoring)
├── follower_client.py (trade execution)
└── notifications.py (alerts)
```

### Setup Dependencies
```
setup.py
├── kiteconnect (Zerodha API)
├── cryptography (credential encryption)
└── python-dotenv (environment management)
```

### Utility Dependencies
```
smart_position_check.py
├── kiteconnect (API access)
├── cryptography (decryption)
└── getpass (secure input)
```

## 📈 Scalability Design

### Multi-Account Support
- Single master account
- Multiple follower accounts
- Individual risk settings per follower
- Segment-specific configurations

### Performance Features
- Asynchronous notifications
- Connection pooling
- Automatic reconnection
- Rate limiting compliance

### Monitoring Features
- Comprehensive logging
- Real-time status reporting
- Performance metrics
- Error tracking

## 🚨 Important Notes

### File Permissions
```bash
# Secure your configuration
chmod 600 .env
chmod 700 kitecopytrader/
```

### Backup Strategy
```bash
# Backup your configuration (exclude credentials from git)
cp .env .env.backup
tar -czf backup_$(date +%Y%m%d).tar.gz *.py *.md requirements.txt
```

### Development Workflow
```bash
# For development
cp .env .env.development
PAPER_TRADING=True python main.py

# For testing
python demo/multi_segment_example.py
python demo/test_notifications.py
```

## 🔄 Maintenance Schedule

### Daily
- Refresh access tokens (`refresh_tokens.py`)
- Check account positions (`smart_position_check.py`)
- Review trading logs

### Weekly
- Backup configuration files
- Review system performance
- Update access tokens if needed

### Monthly
- Review and update dependencies
- System security audit
- Performance optimization review

---

**Quick Start**: Read `Setup_and_Use.md` → Run `setup.py` → Test with `smart_position_check.py` → Start with `main.py`

**Support**: All documentation is in the root directory. Demo files are for learning and testing.