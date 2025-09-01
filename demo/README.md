# Demo & Testing Tools for Zerodha Copy Trading System

This directory contains examples, testing utilities, and development tools to help you understand and test the copy trading system.

---

## 📁 Directory Contents

### 🎯 **Examples & Demonstrations**
- **`multi_segment_example.py`** - Demonstrates multi-segment trading across all exchanges
- **`test_notifications.py`** - Tests the notification system (WhatsApp, Telegram, Email, Discord)

### 🧪 **Testing Utilities**
- **`.env.test`** - Test environment configuration
- **`start.sh`** - Quick start script for demos

### 🛠️ **Utility Scripts** (in utils/ folder)
- **`position_viewer.py`** - Comprehensive position and holdings analyzer
- **`quick_positions.py`** - Quick position checker for encrypted credentials
- **`simple_positions.py`** - Basic position viewer with plain credentials

### 📚 **Documentation**
- **`readme-documentation-backup.md`** - Backup of extended documentation

### 🧹 **Maintenance**
- **`cleanup.py`** - System cleanup and maintenance utility
- **`CLEANUP_COMPLETE.txt`** - Cleanup status indicator

---

## 🚀 Getting Started with Demos

### 1. Multi-Segment Trading Demo
```bash
cd kitecopytrader/demo
python multi_segment_example.py
```

**What it shows:**
- How trades are processed across NSE, BSE, NFO, MCX, BFO, CDS
- Segment-specific risk management
- Different multipliers and limits per segment
- Follower configuration examples

### 2. Notification System Test
```bash
python test_notifications.py
```

**What it tests:**
- WhatsApp notifications via Twilio
- Telegram bot messages
- Email alerts
- Discord webhooks
- Message formatting for different event types

### 3. Position Analysis Tools
```bash
# Comprehensive analysis
python utils/position_viewer.py

# Quick check with smart credential detection
python utils/simple_positions.py

# For encrypted credentials specifically
python utils/quick_positions.py
```

---

## 🎯 Demo Scenarios

### Conservative Trading Setup
```bash
# Demo configuration in .env.test
FOLLOWER_1_NSE_MULTIPLIER=0.1      # 10% of master quantity
FOLLOWER_1_NFO_MULTIPLIER=0.05     # 5% for F&O (leverage risk)
FOLLOWER_1_MCX_MULTIPLIER=0.02     # 2% for commodities (high value)
PAPER_TRADING=True                 # Safe testing mode
```

### Multi-Account Demo
The multi-segment example shows how different follower profiles work:
- **Conservative Follower**: Only equity and currency
- **Aggressive Follower**: All segments with different multipliers  
- **Commodity Specialist**: Focus on MCX and CDS only

---

## 🧪 Testing Workflow

### Phase 1: Understanding the System
1. **Read the code**: Start with `multi_segment_example.py`
2. **Run demonstrations**: See how different segments are handled
3. **Test utilities**: Use position viewers to understand API interaction

### Phase 2: Configuration Testing
1. **Modify `.env.test`**: Try different settings
2. **Test risk management**: See how limits are enforced
3. **Notification testing**: Verify alert systems work

### Phase 3: Integration Testing
1. **Paper trading**: Test with real API but no actual trades
2. **Monitor logs**: Watch system behavior
3. **Performance testing**: Check response times and reliability

---

## 🔧 Utility Scripts Guide

### Position Viewer (`utils/position_viewer.py`)
**Features:**
- Loads credentials from environment or manual input
- Shows positions, holdings, and margins
- Supports both encrypted and plain credentials
- Detailed formatting and currency conversion

**Usage:**
```bash
python utils/position_viewer.py
```

### Simple Position Checker (`utils/simple_positions.py`)
**Features:**
- Clean, user-friendly interface
- Manual credential input
- Quick position summary
- Automatic currency formatting

**Usage:**
```bash
python utils/simple_positions.py
```

### Quick Positions (`utils/quick_positions.py`)
**Features:**
- Specifically designed for encrypted credentials
- Built-in decryption handling
- Optimized for speed
- Error recovery

**Usage:**
```bash
python utils/quick_positions.py
```

---

## 🎮 Interactive Demos

### Multi-Segment Trading Simulation
```bash
python multi_segment_example.py
```

**Sample Output:**
```
NSE EQUITY TRADE: RELIANCE
  Action: BUY 100 shares
  Conservative Follower: 100 → 50 (Within limits)
  Aggressive Follower: 100 → 100 (Within limits)
  
MCX COMMODITY TRADE: GOLD24DECFUT
  Action: BUY 1 lot
  Conservative Follower: SEGMENT DISABLED
  Commodity Specialist: 1 → 5 lots (Within limits)
```

### Notification Demo
```bash
python test_notifications.py
```

**Sample Notifications:**
- **Trade Alert**: "✅ NSE TRADE EXECUTED - RELIANCE BUY 100 @ ₹2,500"
- **System Alert**: "⚠️ WebSocket reconnection in progress"
- **Daily Summary**: "📊 Today: 15 trades, 95% success rate"

---

## ⚙️ Configuration Examples

### Demo Environment (`.env.test`)
```bash
# Conservative demo setup
MASTER_API_KEY=demo_encrypted_key
MASTER_API_SECRET=demo_encrypted_secret
FOLLOWER_COUNT=1
FOLLOWER_1_MULTIPLIER=0.1          # Very small for testing
PAPER_TRADING=True                 # Safety first!
LOG_LEVEL=DEBUG                    # Detailed logging
```

### Testing Different Scenarios
```bash
# High-frequency trading simulation
CHECK_INTERVAL=0.5                 # Check every 500ms
MAX_DAILY_TRADES=200              # Higher limit

# Conservative risk management
FOLLOWER_1_NSE_LIMIT=50           # Small position limits
FOLLOWER_1_NFO_LIMIT=10           # Very small for F&O
RISK_MANAGEMENT=True              # All checks enabled
```

---

## 🎯 Learning Path

### Beginner
1. **Start here**: `multi_segment_example.py`
2. **Understand segments**: Learn NSE, BSE, NFO, MCX, BFO, CDS differences
3. **Test position viewers**: `utils/simple_positions.py`
4. **Paper trading**: Run main system in demo mode

### Intermediate  
1. **Risk management**: Study how limits are enforced
2. **Notification setup**: Configure and test alerts
3. **Multi-account**: Understand follower configurations
4. **Error handling**: See how system recovers from issues

### Advanced
1. **Custom modifications**: Extend risk management rules
2. **Performance optimization**: Network and execution tuning  
3. **Database integration**: Add trade logging
4. **Production deployment**: Security and monitoring setup

---

## 🚨 Safety Notes

### Demo Safety Features
- **Paper trading enabled** by default in all demos
- **Small multipliers** to minimize any accidental impact
- **Conservative limits** on all position sizes
- **Clear logging** to track all activities

### Best Practices
1. **Always test first**: Never skip the demo phase
2. **Start small**: Use tiny multipliers initially  
3. **Monitor actively**: Watch logs and system behavior
4. **Backup config**: Save working configurations
5. **Document changes**: Keep track of modifications

---

## 🔍 Troubleshooting Demos

### Common Issues
1. **Import errors**: Ensure you're in the correct directory
2. **Missing credentials**: Check `.env.test` configuration
3. **API connectivity**: Test with position viewers first
4. **Permission errors**: Check file permissions

### Debug Tips
```bash
# Run with detailed logging
LOG_LEVEL=DEBUG python multi_segment_example.py

# Test API connectivity
python utils/simple_positions.py

# Check configuration
grep -v "^#" .env.test | grep -v "^$"
```

---

## 📈 Performance Testing

### Load Testing
The demos can help you understand system performance:
- **Response times**: How quickly trades are processed
- **Connection stability**: WebSocket reliability
- **Error rates**: How often issues occur
- **Resource usage**: CPU and memory consumption

### Metrics to Watch
- **Trade latency**: Time from detection to replication
- **Success rate**: Percentage of successful replications
- **Connection uptime**: WebSocket availability
- **Memory usage**: System resource consumption

---

## 🎓 Educational Value

### Learning Objectives
1. **Market segments**: Understand Indian stock market structure
2. **Risk management**: Learn position sizing and limits
3. **Real-time systems**: WebSocket and event processing
4. **API integration**: Zerodha KiteConnect usage
5. **System design**: Scalable trading architecture

### Code Study
- **Clean architecture**: Separation of concerns
- **Error handling**: Robust failure recovery
- **Security practices**: Credential protection
- **Performance optimization**: Efficient processing
- **Documentation**: Comprehensive commenting

---

## 📞 Support

### Demo-Specific Help
- **Stuck on setup?** Start with `utils/simple_positions.py`
- **Credentials issues?** Use the smart detection tools
- **Want to understand segments?** Run `multi_segment_example.py`
- **Need to test notifications?** Try `test_notifications.py`

### Next Steps
After mastering the demos:
1. **Main documentation**: Read `../Setup_and_Use.md`
2. **Real setup**: Run `../setup.py`
3. **Live testing**: Use `../smart_position_check.py`
4. **Production**: Start with `../main.py` in paper mode

---

**Remember**: These demos are for learning and testing. Always use paper trading mode when experimenting!

*Happy Trading! 🚀*