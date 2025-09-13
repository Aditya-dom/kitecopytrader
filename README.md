# Zerodha Copy Trading System

**Professional Multi-Segment Copy Trading for Indian Stock Markets**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Educational-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Zerodha-orange.svg)](https://zerodha.com)

---

## 🚀 Quick Start

### For Beginners
1. **Read the complete guide**: [`docs/Setup_and_Use.md`](docs/Setup_and_Use.md) 📖
2. **Run setup**: `python scripts/setup.py` ⚙️
3. **Test first**: `python utils/smart_position_check.py` 🧪
4. **Start trading**: `python run.py` (paper mode) 📈

### For Experienced Traders
```bash
pip install -r requirements.txt
python scripts/setup.py                    # Interactive setup
python utils/smart_position_check.py       # Verify credentials & positions
python scripts/start_real_trading.py       # Live trading (after testing)
```

---

## ⚡ What This System Does

**Automatically replicates trades from a master Zerodha account to multiple follower accounts** across all major Indian market segments in **real-time**.

### 📊 Supported Market Segments
- **NSE Equity** - National Stock Exchange stocks
- **BSE Equity** - Bombay Stock Exchange stocks  
- **NFO** - NSE Futures & Options
- **MCX** - Commodities (Gold, Silver, Crude Oil, etc.)
- **BFO** - BSE Futures & Options
- **CDS** - Currency Derivatives

---

## 🌟 Key Features

### ⚡ Real-Time Trading
- **WebSocket monitoring** of master account
- **Instant trade replication** (sub-second latency)
- **All order types** supported (Market, Limit, SL, etc.)
- **Automatic reconnection** on network issues

### 🛡️ Advanced Risk Management
- **Segment-specific position limits** and multipliers
- **High-risk asset detection** (commodities, volatile stocks)
- **Daily trade and loss limits**
- **Paper trading mode** for safe testing
- **Emergency stop** capabilities

### 🔔 Smart Notifications
- **WhatsApp** alerts via Twilio API
- **Telegram** bot integration
- **Email** notifications with trade details
- **Discord** webhooks for team coordination
- **Real-time status updates** with P&L tracking

### 🔒 Security-First Design
- **Encrypted credential storage** using Fernet encryption
- **Environment-based configuration**
- **No hardcoded secrets**
- **Git protection** for sensitive files
- **Secure token management**

### 🎯 Multi-Account Support
- **1 master → multiple followers** architecture
- **Individual risk settings** per follower
- **Segment enable/disable** per account
- **Custom multipliers** for position sizing
- **Independent monitoring** and controls

---

## 📁 Project Structure

```
kitecopytrader/
├── 📄 README.md                 # This overview
├── 📄 run.py                    # Main entry point
├── 📄 requirements.txt          # Dependencies
├── 🔐 .env                      # Your configuration (not in git)
│
├── 📂 core/                     # Core trading system
│   ├── main.py                  # System orchestrator
│   ├── config.py                # Configuration management
│   ├── master_client.py         # Trade monitoring
│   ├── follower_client.py       # Trade execution
│   └── notifications.py         # Alert system
│
├── 📂 utils/                    # Utility scripts
│   ├── smart_position_check.py  # Position viewer & credential tester
│   ├── check_positions.py       # Position checker
│   ├── refresh_tokens.py        # Daily token refresh
│   ├── automated_token_generator.py  # Automated token generation
│   └── config_loader.py         # Configuration loading utility
│
├── 📂 scripts/                  # Setup and maintenance
│   ├── setup.py                 # Interactive setup wizard
│   ├── setup_config.py          # Configuration setup helper
│   └── start_real_trading.py    # Live trading launcher
│
├── 📂 config/                   # Configuration templates and samples
│   ├── kite_config.json.sample  # Simple Kite configuration template
│   ├── complete_config.json.sample  # Complete configuration template
│   └── automated_credentials.env.sample  # Automated system credentials
│
├── 📂 docs/                     # All documentation
│   ├── Setup_and_Use.md         # COMPLETE SETUP GUIDE - START HERE
│   ├── PROJECT_STRUCTURE.md     # Detailed file organization
│   ├── NOTIFICATION_SETUP.md    # Notification configuration
│   ├── AUTOMATED_TOKEN_GENERATOR.md  # Automated token generation guide
│   └── TESTING.md               # Comprehensive testing guide
│
├── 📂 tests/                      # Comprehensive test suite
│   ├── test_automated_token_generator.py  # Automated system tests
│   ├── test_core_system.py       # Core system component tests
│   ├── test_runner.py            # Main test runner
│   ├── test_config.py            # Test configuration and utilities
│   └── __init__.py               # Test package initialization
│
└── 📂 demo/                     # Examples, tests, and utilities
```

**📖 For detailed structure information, see [`docs/PROJECT_STRUCTURE.md`](docs/PROJECT_STRUCTURE.md)**

---

## 🛠️ Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Interactive Setup (Recommended)
```bash
python scripts/setup.py
```

### 2b. Alternative: JSON Configuration Setup
```bash
# Simple configuration (Kite + Telegram)
python scripts/setup_config.py

# Choose 'simple' for basic setup
# Choose 'complete' for full copy trading setup
```

### 3. Test Your Configuration
```bash
python utils/smart_position_check.py
```

### 4. Test Your Setup
```bash
# Run quick tests to verify everything works
python run_tests.py --quick

# Run full test suite
python run_tests.py
```

### 5. Start Trading
```bash
# Paper trading (safe testing)
PAPER_TRADING=True python run.py

# Live trading (after thorough testing)
python scripts/start_real_trading.py
```

---

## 📚 Documentation

- **[docs/Setup_and_Use.md](docs/Setup_and_Use.md)** - Complete setup and usage guide
- **[docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)** - File organization details
- **[docs/NOTIFICATION_SETUP.md](docs/NOTIFICATION_SETUP.md)** - Notification configuration
- **[demo/README.md](demo/README.md)** - Examples and testing tools

---

## 🚨 Important Warnings

### Financial Risks
- **Capital at Risk**: Trading involves substantial risk of loss
- **Leverage Risk**: F&O and commodities can amplify losses rapidly
- **System Risk**: Technical failures may result in trading errors
- **Market Risk**: Volatile markets can cause significant losses

### Technical Considerations
- **Internet Dependency**: Stable connection required for real-time operation
- **Token Management**: Access tokens expire daily and must be refreshed
- **API Limits**: Zerodha has rate limits that must be respected
- **Testing Critical**: Thorough testing required before live trading

---

## 🎯 Getting Started Checklist

- [ ] **Read** [`docs/Setup_and_Use.md`](docs/Setup_and_Use.md) completely
- [ ] **Install** Python 3.7+ and dependencies
- [ ] **Obtain** Zerodha API credentials
- [ ] **Run** `python scripts/setup.py` for interactive setup
- [ ] **Test** with `python utils/smart_position_check.py`
- [ ] **Verify** paper trading: `PAPER_TRADING=True python run.py`
- [ ] **Monitor** for several days before considering live trading
- [ ] **Start small** with conservative multipliers
- [ ] **Scale gradually** after gaining confidence

---

**⚠️ CRITICAL**: This system trades with real money. Always test thoroughly with paper trading before live deployment. You are fully responsible for all trades and their outcomes.

**🎯 SUCCESS TIP**: Start with `PAPER_TRADING=True` and very small multipliers (0.01-0.05) when you first go live.

---

*For detailed setup instructions, see [`docs/Setup_and_Use.md`](docs/Setup_and_Use.md)*
*For file organization details, see [`docs/PROJECT_STRUCTURE.md`](docs/PROJECT_STRUCTURE.md)*
