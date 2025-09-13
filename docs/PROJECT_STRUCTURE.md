# Zerodha Copy Trading System

## 📁 Directory Structure

```
kitecopytrader/
├── 📄 README.md                    # Main project overview
├── 📄 run.py                      # Main entry point (replaces main.py)
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore                  # Git security - protects sensitive files
├── 📄 .env                        # Main configuration (NOT in git)
├── 📄 __init__.py                 # Package initialization
│
├── 📂 core/                       # Core trading system
│   ├── 📄 __init__.py             # Core module initialization
│   ├── 📄 main.py                 # System orchestrator and launcher
│   ├── 📄 config.py               # Configuration management
│   ├── 📄 master_client.py        # Master account monitoring
│   ├── 📄 follower_client.py      # Trade replication engine
│   └── 📄 notifications.py        # Multi-channel notification system
│
├── 📂 utils/                      # Utility scripts and tools
│   ├── 📄 __init__.py             # Utils module initialization
│   ├── 📄 smart_position_check.py # Position viewer & credential tester
│   ├── 📄 check_positions.py      # Position checker for encrypted credentials
│   └── 📄 refresh_tokens.py       # Daily token refresh utility
│
├── 📂 scripts/                    # Setup and maintenance scripts
│   ├── 📄 __init__.py             # Scripts module initialization
│   ├── 📄 setup.py                # Interactive system setup wizard
│   └── 📄 start_real_trading.py   # Live trading launcher with safety checks
│
├── 📂 config/                     # Configuration templates and samples
│   ├── 📄 __init__.py             # Config module initialization
│   └── 📄 (config templates)      # Sample configuration files
│
├── 📂 docs/                       # All documentation
│   ├── 📄 README.md               # Main project overview
│   ├── 📄 PROJECT_STRUCTURE.md    # This file - project organization
│   ├── 📄 Setup_and_Use.md        # Complete setup and usage guide
│   └── 📄 NOTIFICATION_SETUP.md   # Notification system setup guide
│
├── 📂 tests/                      # Test files and examples
│   └── 📄 (test files)            # Unit tests and integration tests
│
└── 📂 demo/                       # Examples, tests, and utilities
    ├── 📄 README.md               # Demo documentation
    ├── 📄 multi_segment_example.py # Multi-segment trading demonstration
    ├── 📄 test_notifications.py   # Notification system testing
    ├── 📄 cleanup.py              # System cleanup utility
    ├── 📄 start.sh                # Demo startup script
    └── 📂 utils/                  # Demo utility scripts
        ├── 📄 position_viewer.py  # Detailed position analysis
        ├── 📄 quick_positions.py  # Quick position checker
        └── 📄 simple_positions.py # Simple position viewer
```

## 🎯 Module Organization

### 🚀 **Core Module** (`core/`)
Contains the main trading system components:
- **`main.py`** - Central orchestrator and system launcher
- **`config.py`** - Configuration management and security
- **`master_client.py`** - WebSocket monitoring of master account
- **`follower_client.py`** - Trade replication for follower accounts
- **`notifications.py`** - Multi-channel notification system

### 🛠️ **Utils Module** (`utils/`)
Contains utility scripts and helper functions:
- **`smart_position_check.py`** - Position viewer and credential tester
- **`check_positions.py`** - Position checker for encrypted credentials
- **`refresh_tokens.py`** - Daily access token refresh utility

### 📜 **Scripts Module** (`scripts/`)
Contains setup and maintenance scripts:
- **`setup.py`** - Interactive system setup wizard
- **`start_real_trading.py`** - Live trading launcher with safety checks

### 📚 **Docs Module** (`docs/`)
Contains all documentation:
- **`README.md`** - Main project overview
- **`Setup_and_Use.md`** - Complete setup and usage guide
- **`PROJECT_STRUCTURE.md`** - This file
- **`NOTIFICATION_SETUP.md`** - Notification configuration help

### ⚙️ **Config Module** (`config/`)
Contains configuration templates and samples:
- Configuration templates
- Environment variable management
- Sample configuration files

## 🔄 Updated Usage Workflow

### 1. **First Time Setup**
```bash
# Read the documentation first
cat docs/Setup_and_Use.md

# Run interactive setup
python scripts/setup.py
```

### 2. **Daily Trading Routine**
```bash
# Morning: Refresh tokens
python utils/refresh_tokens.py

# Check account status
python utils/smart_position_check.py

# Start trading (paper mode first!)
python run.py

# Or for live trading (after thorough testing)
python scripts/start_real_trading.py
```

### 3. **Monitoring and Maintenance**
```bash
# Check logs
tail -f copy_trader.log

# Emergency stop
Ctrl+C in the terminal running run.py
```

## 📦 Package Structure Benefits

### ✅ **Improved Organization**
- Clear separation of concerns
- Easy to navigate and maintain
- Professional project structure
- Scalable architecture

### ✅ **Better Imports**
- Clean import statements
- No circular dependencies
- Proper Python package structure
- Easy to extend and modify

### ✅ **Enhanced Security**
- Sensitive files in appropriate locations
- Clear separation of public and private code
- Better access control
- Improved maintainability

### ✅ **Developer Experience**
- Intuitive file organization
- Easy to find specific functionality
- Clear module boundaries
- Better code reusability

## 🔧 Migration Notes

### **What Changed:**
1. **Main entry point**: `main.py` → `run.py` (in root)
2. **Core files**: Moved to `core/` directory
3. **Utilities**: Moved to `utils/` directory
4. **Scripts**: Moved to `scripts/` directory
5. **Documentation**: Moved to `docs/` directory
6. **Imports**: Updated to use relative imports

### **What Stayed the Same:**
1. **Functionality**: All features work exactly the same
2. **Configuration**: Same `.env` file and settings
3. **API**: Same command-line interface
4. **Logs**: Same logging and output

### **New Entry Points:**
- **Main system**: `python run.py` (instead of `python main.py`)
- **Setup**: `python scripts/setup.py` (same as before)
- **Utilities**: `python utils/smart_position_check.py` (same as before)

## 🚀 Quick Start with New Structure

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run setup
python scripts/setup.py

# 3. Test configuration
python utils/smart_position_check.py

# 4. Start trading
python run.py
```

## 📋 File Dependencies

### Core Dependencies
```
run.py
└── core/
    ├── main.py (system orchestrator)
    ├── config.py (configuration)
    ├── master_client.py (trade monitoring)
    ├── follower_client.py (trade execution)
    └── notifications.py (alerts)
```

### Setup Dependencies
```
scripts/setup.py
├── kiteconnect (Zerodha API)
├── cryptography (credential encryption)
└── python-dotenv (environment management)
```

### Utility Dependencies
```
utils/smart_position_check.py
├── kiteconnect (API access)
├── cryptography (decryption)
└── getpass (secure input)
```

---

**Quick Start**: Read `docs/Setup_and_Use.md` → Run `scripts/setup.py` → Test with `utils/smart_position_check.py` → Start with `run.py`

**Support**: All documentation is in the `docs/` directory. Demo files are for learning and testing.