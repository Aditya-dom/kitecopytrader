# Zerodha Copy Trading System

A secure, robust and copy trading application for Zerodha Kite that replicates trades from a master account to multiple follower accounts in real-time.

**READ THIS CAREFULLY BEFORE USING:**

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

### 1. Installation

```bash
# Clone or download the system files
# Install Python 3.8+ if not already installed

# Run the automated setup
python setup.py
```

The setup script will:
- Install all required packages
- Guide you through account configuration
- Generate secure configuration files
- Set up paper trading mode by default

### 2. Manual Installation

If you prefer manual setup:

```bash
# Install requirements
pip install -r requirements.txt

# Copy environment template
cp .env.sample .env

# Edit .env with your credentials
nano .env
```

### 3. Configuration

#### Environment Variables Method (Recommended)

Edit your `.env` file:

```bash
# Master Account
MASTER_API_KEY=your_master_api_key
MASTER_API_SECRET=your_master_api_secret
MASTER_ACCESS_TOKEN=your_master_access_token
MASTER_USER_ID=your_master_user_id

# Follower Account 1
FOLLOWER_COUNT=1
FOLLOWER_1_API_KEY=your_follower_api_key
FOLLOWER_1_API_SECRET=your_follower_api_secret
FOLLOWER_1_ACCESS_TOKEN=your_follower_access_token
FOLLOWER_1_USER_ID=your_follower_user_id
FOLLOWER_1_MULTIPLIER=1.0
FOLLOWER_1_MAX_POSITION=1000
FOLLOWER_1_ENABLED=True

# System Settings
PAPER_TRADING=True  # KEEP THIS TRUE FOR TESTING
LOG_LEVEL=INFO
```

### 4. Getting API Credentials

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

### 5. Running the System

```bash
# Start the copy trading system
python main.py
```

**First run checklist:**
- ✅ Paper trading mode should be enabled
- ✅ Verify all account connections
- ✅ Monitor logs for any errors
- ✅ Test with small position sizes

---

## System Architecture

### Core Components

#### 1. `config.py` - Secure Configuration Management
- Handles API credentials securely
- Supports encryption for sensitive data
- Environment variable integration
- Configuration validation

#### 2. `master_client.py` - Master Account Monitor  
- WebSocket connection to Kite Connect
- Real-time order update monitoring
- Automatic reconnection handling
- Trade filtering and validation

#### 3. `follower_client.py` - Follower Account Manager
- Order placement for follower accounts
- Risk management and position limits
- Retry logic for failed orders
- Account-specific settings

#### 4. `main.py` - System Controller
- Orchestrates master and follower clients
- System health monitoring
- Graceful shutdown handling
- Statistics and logging

### Data Flow

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

## Configuration Options

### Master Account Settings
- `MASTER_API_KEY`: Your Kite Connect API key
- `MASTER_API_SECRET`: Your API secret (encrypted)
- `MASTER_ACCESS_TOKEN`: Access token (encrypted)
- `MASTER_USER_ID`: Your user ID

### Follower Account Settings
- `FOLLOWER_COUNT`: Number of follower accounts
- `FOLLOWER_X_API_KEY`: API key for follower X
- `FOLLOWER_X_MULTIPLIER`: Quantity multiplier (e.g., 0.5 = half size)
- `FOLLOWER_X_MAX_POSITION`: Maximum position size
- `FOLLOWER_X_ENABLED`: Enable/disable this follower

### System Settings
- `PAPER_TRADING`: Enable simulation mode (True/False)
- `CHECK_INTERVAL`: WebSocket check interval in seconds
- `MAX_RETRIES`: Maximum retry attempts for failed operations
- `LOG_LEVEL`: Logging verbosity (DEBUG/INFO/WARNING/ERROR)
- `MAX_DAILY_TRADES`: Maximum trades per day per follower

### Security Settings
- `ENCRYPTION_KEY`: Key for encrypting sensitive data
- Support for HashiCorp Vault or AWS Secrets Manager

---

## Risk Management Features

### Position Limits
- **Maximum Position Size**: Limit per instrument per account
- **Daily Trade Limits**: Maximum number of trades per day
- **Quantity Multipliers**: Scale trade sizes based on account capital

### Error Handling
- **API Rate Limiting**: Automatic retry with exponential backoff
- **Connection Recovery**: Automatic WebSocket reconnection
- **Order Validation**: Verify all order parameters before placement
- **Insufficient Funds**: Handle margin-related errors gracefully

### Monitoring
- **Real-time Status**: Connection health and trade counts
- **Performance Metrics**: Success/failure rates and timing
- **Alert System**: Notifications for critical errors
- **Daily Statistics**: Reset counters at market open

---

## Usage Guide

### Starting the System

1. **Pre-flight Checklist**:
   ```bash
   # Verify configuration
   python -c "from config import SecureConfigManager; print('Config OK')"
   
   # Test API connections
   python -c "from main import main; main()" --test-only
   ```

2. **Start Copy Trading**:
   ```bash
   python main.py
   ```

3. **Monitor Logs**:
   ```bash
   # Watch real-time logs
   tail -f copy_trader.log
   
   # Filter for errors only
   grep ERROR copy_trader.log
   ```

### Testing Strategy

#### Phase 1: Paper Trading (Mandatory)
```bash
# Ensure paper trading is enabled
PAPER_TRADING=True python main.py
```

- Run for at least 1 week during market hours
- Verify all trades are detected correctly
- Check that follower orders would be placed correctly
- Monitor for any connection issues or errors

#### Phase 2: Small Live Testing  
```bash
# Very small quantities only
FOLLOWER_1_MULTIPLIER=0.1  # 10% of master size
FOLLOWER_1_MAX_POSITION=10  # Maximum 10 shares
PAPER_TRADING=False python main.py
```

#### Phase 3: Gradual Scale-up
- Increase multipliers gradually
- Monitor performance closely
- Keep detailed records of all trades

### Market Hours Operation

The system automatically:
- **Detects market hours**: 9:15 AM - 3:30 PM IST, Monday-Friday
- **Blocks weekend trading**: No trades on Saturday/Sunday  
- **Handles holidays**: Market holiday detection (configure manually)

### Daily Operations

#### Market Open (9:15 AM)
- System resets daily statistics
- Clears processed order cache
- Validates all account connections

#### During Market Hours
- Continuous monitoring and replication
- Real-time logging of all activities
- Automatic error recovery

#### Market Close (3:30 PM)
- System continues monitoring (for after-hours updates)
- Daily statistics logged
- Access tokens remain valid until next day

#### After Market Close
- Review daily performance
- Check for any failed orders
- Prepare for next trading day

---

## Troubleshooting

### Common Issues

#### 1. Connection Errors
```
Error: WebSocket connection failed
```
**Solution**:
- Check internet connectivity
- Verify API credentials
- Ensure access tokens are not expired
- Check Zerodha server status

#### 2. Authentication Errors
```
Error: Invalid access token
```
**Solution**:
- Access tokens expire daily
- Generate new tokens using the login flow
- Update `.env` file with new tokens

#### 3. Order Placement Failures
```
Error: Insufficient funds
```
**Solution**:
- Check available margin in follower accounts
- Reduce position sizes or multipliers
- Ensure accounts have adequate balance

#### 4. API Rate Limiting
```
Error: Too many requests
```
**Solution**:
- System has built-in rate limiting
- Check if multiple instances are running
- Reduce check interval if needed

### Debug Mode

Enable detailed debugging:
```bash
LOG_LEVEL=DEBUG python main.py
```

This will log:
- All WebSocket messages
- Order placement attempts  
- Risk management decisions
- Connection status changes

### Log Analysis

Important log patterns to monitor:

```bash
# Successful trade replication
grep "Trade replicated successfully" copy_trader.log

# Connection issues
grep "WebSocket" copy_trader.log

# Risk management blocks  
grep "blocked by risk management" copy_trader.log

# Order failures
grep "Failed to replicate trade" copy_trader.log
```

---

## Advanced Configuration

### Custom Risk Management

Extend the `FollowerAccountClient` class:

```python
class CustomFollowerClient(FollowerAccountClient):
    def _check_risk_limits(self, trade_data):
        # Add custom risk checks
        symbol = trade_data['tradingsymbol']
        
        # Block penny stocks
        if 'PENNY' in symbol:
            return False, "Penny stocks not allowed"
            
        # Custom position limits by sector
        if symbol.startswith('IT'):
            max_qty = 500
        else:
            max_qty = 1000
            
        # Call parent risk checks
        return super()._check_risk_limits(trade_data)
```

### Multiple Master Accounts

For advanced setups with multiple master accounts:

```python
# Create multiple master clients
master_clients = [
    MasterAccountClient(master_config_1, callback_1),
    MasterAccountClient(master_config_2, callback_2)
]

# Start all masters
for master in master_clients:
    master.start_monitoring()
```

### Database Integration

Add trade logging to database:

```python
import sqlite3

class DatabaseLogger:
    def __init__(self, db_path="trades.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                master_user_id TEXT,
                follower_user_id TEXT,
                symbol TEXT,
                quantity INTEGER,
                price REAL,
                status TEXT
            )
        """)
    
    def log_trade(self, trade_data):
        # Log trade to database
        pass
```

### Notification System

Add alerts for important events:

```python
import smtplib
from email.mime.text import MIMEText

class NotificationSystem:
    def __init__(self, email_config):
        self.email_config = email_config
    
    def send_alert(self, message):
        # Send email alert
        msg = MIMEText(message)
        msg['Subject'] = 'Copy Trading Alert'
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']
        
        # Send email...
```

---

## Performance Optimization

### WebSocket Optimization
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

### Network Considerations
- Low-latency internet connection
- Backup internet connection (4G/5G)
- Close to Zerodha servers geographically

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

### Access Control
- Limit file permissions (chmod 600 .env)
- Use dedicated user account for the system
- Log all access attempts
- Regular security audits

---

### Documentation Requirements
- **Trade Records**: All executed trades with timestamps
- **System Logs**: Complete audit trail
- **Risk Management**: Documentation of risk controls
- **Performance Reports**: Regular performance reporting

### Compliance Checklist
- [ ] Legal consultation completed
- [ ] Regulatory registrations obtained (if required)
- [ ] Client agreements in place
- [ ] Risk disclosure provided
- [ ] Audit systems implemented
- [ ] Compliance monitoring active

---

## API Limits and Quotas

### Zerodha Kite Connect Limits
- **Order placement**: 3 orders per second
- **API calls**: 3 calls per second
- **WebSocket**: 3 concurrent connections per API key
- **Daily limits**: Check Zerodha documentation for current limits

### Rate Limiting Strategy
```python
import time
from functools import wraps

def rate_limit(max_calls_per_second=3):
    min_interval = 1.0 / max_calls_per_second
    last_call_time = [0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            time_since_last_call = current_time - last_call_time[0]
            
            if time_since_last_call < min_interval:
                time.sleep(min_interval - time_since_last_call)
            
            result = func(*args, **kwargs)
            last_call_time[0] = time.time()
            return result
        return wrapper
    return decorator
```

---

## Monitoring and Alerting

### Key Metrics to Monitor
- **Trade Replication Success Rate**: Should be >95%
- **WebSocket Connection Uptime**: Should be >99%
- **Order Execution Latency**: Average time from detection to placement
- **Daily PnL**: Track performance across all accounts
- **Error Rates**: Monitor different types of errors

### Dashboard Setup
Create a simple monitoring dashboard:

```python
import flask
from flask import render_template

app = flask.Flask(__name__)

@app.route('/dashboard')
def dashboard():
    # Get system statistics
    stats = copy_system.get_system_stats()
    return render_template('dashboard.html', stats=stats)

# Run dashboard
app.run(host='0.0.0.0', port=5000)
```

### Alerting Rules
- **Connection Lost**: Alert if WebSocket disconnected >30 seconds
- **High Error Rate**: Alert if >5% of orders fail
- **Daily Loss Limit**: Alert if daily losses exceed threshold
- **System Errors**: Alert on any critical system errors

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

### Recovery Testing
- Test backup restoration quarterly
- Verify all credentials work after restoration
- Practice manual override procedures
- Document recovery time objectives

---

## Support and Maintenance

### Regular Maintenance Tasks
- **Daily**: Check logs for errors, verify connections
- **Weekly**: Review performance metrics, update documentation
- **Monthly**: Security updates, credential rotation
- **Quarterly**: Full system audit, disaster recovery testing

### Getting Help
1. **Check logs first**: Most issues are logged with details
2. **Review documentation**: Common issues covered here
3. **Test in isolation**: Isolate the problem component
4. **Community support**: Trading forums and communities

### Contributing
If you improve the system:
- Document changes clearly
- Test thoroughly before sharing
- Consider security implications
- Share with the community

---

## License and Legal

### Open Source License
This project is provided as-is for educational and personal use.

### Disclaimer
- No warranty or guarantee of performance
- Users are responsible for all trading decisions
- Not investment advice
- Regulatory compliance is user's responsibility

### Liability Limitation
The authors and contributors are not liable for:
- Trading losses or missed opportunities
- System failures or downtime
- Regulatory violations
- Data breaches or security issues

---

**Remember: Trading involves risk. Never trade more than you can afford to lose. Always test thoroughly and comply with all applicable regulations.**