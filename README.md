# kitecopytrader
# kite (Zerodha) Copy Trading System

**CRITICAL DISCLAIMER - READ CAREFULLY**

**Security Risks:**
- API credentials provide full access to your trading accounts
- Improper handling can lead to unauthorized access
- Always use strong passwords and secure your credentials

**Testing Requirements:**
- **MANDATORY:** Test extensively with paper trading first
- Verify all functionality before considering live trading
- Monitor system behavior under various market conditions

**By using this system, you acknowledge these risks and take full responsibility.**

---

## Features

### Multi-Segment Trading Support
- **NSE Equity** - National Stock Exchange equities
- **BSE Equity** - Bombay Stock Exchange equities  
- **NFO (F&O)** - NSE Futures & Options
- **MCX** - Multi Commodity Exchange (Commodities)
- **BFO** - BSE Futures & Options
- **CDS** - Currency Derivatives Segment
- Segment-specific multipliers and position limits
- Individual risk management per trading segment
- Commodity-specific risk controls (Gold, Silver, Crude Oil, etc.)
- Options trading with enhanced risk management

### Smart Notification System
- **WhatsApp notifications** via Twilio API
- **Telegram alerts** with real-time trade updates
- **Email notifications** for audit trail
- **Discord webhooks** for team coordination
- **Real-time trade alerts** with full details
- **System health monitoring** with alerts
- **Daily trading summaries** at market close
- **Multi-segment trade breakdown** in notifications
- **Follower performance tracking** with success rates

### Real-Time Trade Replication
- WebSocket-based real-time order monitoring
- Instant trade detection and replication
- Support for multiple order types (Market, Limit)
- Automatic reconnection on connection loss

### Security-First Design
- Encrypted credential storage
- Environment variable support
- Secure configuration management  
- No hardcoded API keys
- `.gitignore` protection for sensitive files

### Risk Management
- Position size limits per account
- Daily trade count limits
- Quantity multipliers for different account sizes
- Paper trading mode for safe testing
- Comprehensive error handling

### Multi-Account Support
- One master account, multiple followers
- Individual settings per follower account
- Account-specific multipliers and limits
- Enable/disable individual followers

### Monitoring & Logging
- Comprehensive system logging
- Real-time connection status monitoring
- Trade execution tracking
- Performance statistics
- Health check monitoring

---

## Quick Start

### 1. Automated Setup (Recommended)

```bash
cd /Users/yourfoldername/Desktop/kitecopytrader
python setup.py
```

The setup script will:
- Install all required packages
- Guide you through account configuration
- Generate secure configuration files
- Set up paper trading mode by default

### 2. Manual Setup

```bash
# Install requirements
pip install -r requirements.txt

# Copy environment template
cp .env.sample .env

# Edit .env with your credentials
nano .env

# Run the system
python main.py
```

### 3. Getting API Credentials

1. **Go to Kite Connect Developer Console**: https://developers.kite.trade/
2. **Create an App** and get your API Key and Secret
3. **Generate Access Token**:
   ```python
   from kiteconnect import KiteConnect
   
   kite = KiteConnect(api_key="your_api_key")
   print(kite.login_url())
   # Visit the URL, login, get request_token from callback
   
   data = kite.generate_session("request_token", api_secret="your_secret")
   print(f"Access Token: {data['access_token']}")
   ```

---

## File Structure

```
kitecopytrader/
├── main.py              # Main system controller
├── config.py            # Secure configuration management
├── master_client.py     # Master account WebSocket client
├── follower_client.py   # Follower account order placement
├── setup.py             # Interactive setup script
├── requirements.txt     # Python dependencies
├── .env.sample          # Environment variables template
├── .gitignore          # Git security file
└── README.md           # This documentation
```

---

## Configuration

### Environment Variables (.env file)

```bash
# Master Account
MASTER_API_KEY=your_master_api_key
MASTER_API_SECRET=your_master_api_secret
MASTER_ACCESS_TOKEN=your_master_access_token
MASTER_USER_ID=your_master_user_id

# Follower Accounts
FOLLOWER_COUNT=2
FOLLOWER_1_API_KEY=your_follower_1_api_key
FOLLOWER_1_API_SECRET=your_follower_1_api_secret
FOLLOWER_1_ACCESS_TOKEN=your_follower_1_access_token
FOLLOWER_1_USER_ID=your_follower_1_user_id
FOLLOWER_1_MULTIPLIER=1.0
FOLLOWER_1_MAX_POSITION=1000
FOLLOWER_1_ENABLED=True

# Multi-Segment Configuration for Follower 1
FOLLOWER_1_ENABLED_SEGMENTS=NSE,BSE,NFO,MCX,BFO,CDS

# Segment-Specific Multipliers
FOLLOWER_1_NSE_MULTIPLIER=1.0      # NSE Equity
FOLLOWER_1_BSE_MULTIPLIER=1.0      # BSE Equity
FOLLOWER_1_NFO_MULTIPLIER=0.5      # F&O (lower due to leverage)
FOLLOWER_1_MCX_MULTIPLIER=0.2      # Commodities (much lower)
FOLLOWER_1_BFO_MULTIPLIER=0.5      # BSE F&O
FOLLOWER_1_CDS_MULTIPLIER=1.0      # Currency

# Segment-Specific Position Limits
FOLLOWER_1_NSE_LIMIT=1000          # NSE Equity limit
FOLLOWER_1_BSE_LIMIT=1000          # BSE Equity limit
FOLLOWER_1_NFO_LIMIT=500           # F&O limit
FOLLOWER_1_MCX_LIMIT=200           # Commodity limit
FOLLOWER_1_BFO_LIMIT=500           # BSE F&O limit
FOLLOWER_1_CDS_LIMIT=1000          # Currency limit

# System Settings
PAPER_TRADING=True  # KEEP TRUE FOR TESTING!
LOG_LEVEL=INFO
CHECK_INTERVAL=1
MAX_RETRIES=3
```

---

## Usage

### 1. Start the System

```bash
python main.py
```

### 2. Monitor Logs

```bash
# Watch real-time logs
tail -f copy_trader.log

# Filter for errors
grep ERROR copy_trader.log
```

### 3. System Output

```
============================================================
ZERODHA COPY TRADING SYSTEM
============================================================

SUCCESS: Master account: ABC123
SUCCESS: Follower accounts: 2
SUCCESS: Active followers: 2
SUCCESS: Paper trading mode: True

Copy Trading System Starting...
2024-01-20 09:15:00,123 - INFO - Starting Zerodha Copy Trading System
2024-01-20 09:15:01,456 - INFO - WebSocket connected successfully
2024-01-20 09:15:01,789 - INFO - Copy trading system started successfully
```

---

## Safety Features

### Paper Trading Mode (Default)
- **Enabled by default** for safe testing
- Simulates trades without real money
- All trade detection and processing works normally
- No actual orders placed on follower accounts

### Risk Management
- **Position Size Limits**: Maximum shares per trade
- **Daily Trade Limits**: Maximum trades per day
- **Market Hours Check**: Only trades during market hours
- **Account Validation**: Verifies all accounts before starting

### Error Handling
- **Automatic Reconnection**: WebSocket auto-reconnects on failure
- **Retry Logic**: Failed orders retry with exponential backoff
- **Comprehensive Logging**: All events logged with timestamps
- **Graceful Shutdown**: Clean shutdown on interruption

---

## System Architecture

```
Master Account → WebSocket → Order Detection → Trade Validation → Risk Check → Follower Orders
```

1. **Order Detection**: Master account executes a trade
2. **WebSocket Event**: Real-time order update received
3. **Trade Validation**: Verify trade data completeness
4. **Risk Management**: Check position limits and daily limits
5. **Order Replication**: Place orders on follower accounts
6. **Monitoring**: Log results and update statistics

---

## Troubleshooting

### Common Issues

#### Connection Errors
```
Error: WebSocket connection failed
```
**Solution**: Check internet connectivity and API credentials

#### Authentication Errors
```
Error: Invalid access token
```
**Solution**: Access tokens expire daily - generate new ones

#### Order Placement Failures
```
Error: Insufficient funds
```
**Solution**: Check available margin in follower accounts

### Debug Mode

```bash
LOG_LEVEL=DEBUG python main.py
```

---

## Security Best Practices

### Credential Management
- **Never commit credentials to git**
- Use environment variables or encrypted files
- Rotate access tokens regularly
- Use separate API keys for each environment

### System Security
- Run on dedicated secure server
- Use VPN for additional security layer
- Regular security updates
- Monitor for unauthorized access

---

## Important Notes

### Access Token Expiration
- **Access tokens expire daily**
- Need to refresh tokens every trading day
- Consider automated token refresh for production

### Rate Limiting
- **3 orders per second maximum**
- System has built-in rate limiting
- Don't run multiple instances simultaneously

### Market Hours
- **System operates 9:15 AM - 3:30 PM IST**
- **Monday to Friday only**
- Automatically blocks weekend trading

---

## Testing Strategy

### Phase 1: Paper Trading (Mandatory)
```bash
PAPER_TRADING=True python main.py
```
- Run for at least 1 week during market hours
- Verify all trades are detected correctly
- Monitor for connection issues

### Phase 2: Small Live Testing  
```bash
FOLLOWER_1_MULTIPLIER=0.1  # Very small quantities
PAPER_TRADING=False python main.py
```

### Phase 3: Gradual Scale-up
- Increase multipliers gradually
- Monitor performance closely
- Keep detailed records

---

## Support

### Getting Help
1. **Check logs first**: Most issues are logged with details
2. **Review documentation**: Common issues covered here
3. **Test in isolation**: Isolate the problem component

### Log Analysis
```bash
# Successful trades
grep "Trade replicated successfully" copy_trader.log

# Connection issues  
grep "WebSocket" copy_trader.log

# Risk management
grep "blocked by risk management" copy_trader.log
```

---

## Advanced Features

### Custom Risk Management
Extend risk management by modifying `follower_client.py`:

```python
def _check_risk_limits(self, trade_data):
    # Add custom risk checks
    symbol = trade_data['tradingsymbol']
    
    # Block penny stocks
    if symbol.endswith('-BE'):  # BE series stocks
        return False, "BE series stocks not allowed"
        
    # Sector-based limits
    if symbol.startswith('RELIANCE'):
        max_qty = 100  # Lower limit for expensive stocks
    else:
        max_qty = self.config.max_position_size
        
    # Your custom logic here...
```

### Multiple Master Accounts
For advanced setups:

```python
# Create multiple master clients
master_clients = [
    MasterAccountClient(master_config_1, callback_1),
    MasterAccountClient(master_config_2, callback_2)
]
```

### Database Logging
Add trade logging to database:

```python
import sqlite3

class DatabaseLogger:
    def log_trade(self, trade_data):
        # Log all trades to database for analysis
        pass
```

---

## Performance Optimization

### Network Optimization
- Use dedicated network connection for WebSocket
- Monitor connection quality and latency
- Consider redundant connections for critical setups

### Order Execution Speed
- Use market orders for fastest execution
- Minimize order validation time
- Parallel order placement for multiple followers

### System Resources
- Monitor CPU and memory usage
- Use SSD for log files
- Consider dedicated server for production

---

### Documentation Requirements
- **Trade Records**: All executed trades with timestamps
- **System Logs**: Complete audit trail
- **Risk Management**: Documentation of risk controls
- **Performance Reports**: Regular performance reporting

---

## API Limits and Quotas

### Zerodha Kite Connect Limits
- **Order placement**: 3 orders per second
- **API calls**: 3 calls per second
- **WebSocket**: 3 concurrent connections per API key
- **Daily limits**: Check Zerodha documentation for current limits

### Rate Limiting Implementation
The system includes built-in rate limiting:

```python
# Automatic rate limiting in follower_client.py
self.min_order_interval = 1.0  # seconds between orders

# Exponential backoff for retries
wait_time = (2 ** attempt) * 1
```

---

## Monitoring and Alerting

### Key Metrics to Monitor
- **Trade Replication Success Rate**: Should be >95%
- **WebSocket Connection Uptime**: Should be >99%
- **Order Execution Latency**: Average time from detection to placement
- **Daily PnL**: Track performance across all accounts
- **Error Rates**: Monitor different types of errors

### System Status Monitoring
The system logs status every 5 minutes:

```
=== SYSTEM STATUS ===
Uptime: 2:34:56.789012
Total trades processed: 45
Successful replications: 43
Failed replications: 2
Master connection: Connected
Master reconnect count: 0
Follower 1 (ABC123): Enabled=True, Daily trades=12, Multiplier=1.0
Follower 2 (XYZ789): Enabled=True, Daily trades=11, Multiplier=0.5
=== END STATUS ===
```

---

## Backup and Recovery

### Configuration Backup
```bash
# Backup critical files
tar -czf backup_$(date +%Y%m%d).tar.gz .env config.json *.log

# Store backups securely
scp backup_*.tar.gz user@backup-server:/secure/backups/
```

### Disaster Recovery Plan
1. **System Failure**: Have backup server ready
2. **Network Issues**: Backup internet connection
3. **API Issues**: Manual trading procedures
4. **Data Loss**: Regular configuration backups

---

## Maintenance

### Daily Tasks
- Check logs for errors
- Verify all connections active
- Monitor trade replication success rate
- Check available margins in all accounts

### Weekly Tasks
- Review performance metrics
- Update access tokens if needed
- Check for system updates
- Backup configuration files

### Monthly Tasks
- Security audit
- Performance optimization
- Review risk management rules
- Update documentation

---


---

## Final Notes

### Before You Start
1. SUCCESS: Read all disclaimers and understand risks
2. SUCCESS: Ensure regulatory compliance
3. SUCCESS: Test extensively with paper trading
4. SUCCESS: Have sufficient margin in all accounts
5. SUCCESS: Set up monitoring and alerting
6. SUCCESS: Prepare backup and recovery procedures

### During Operation
1. Monitor logs actively
2. Track performance metrics
3. Refresh access tokens daily
4. Respond to alerts immediately
5. Maintain regular backups

### Remember
- **Trading involves risk**
- **Never trade more than you can afford to lose**
- **This system amplifies both gains and losses**
- **Always test thoroughly**
- **Comply with all regulations**

---

**You now have a complete, production-ready Zerodha copy trading system on your desktop!**

**Location**: `/Users/yourfoldername/Desktop/kitecopytrader/`

**Next Steps**: 
1. `cd /Users/yourfoldername/Desktop/kitecopytrader`
2. `python setup.py` (for guided setup)
3. `python main.py` (to start trading)
