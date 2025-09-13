# Automated Token Generator

**Automated Access Token Generation and Trade Monitoring**

This utility provides automated access token generation using Selenium WebDriver and real-time trade monitoring with Telegram notifications.

## 🚀 Features

### ⚡ Automated Token Generation
- **Selenium WebDriver** automation for Zerodha login
- **TOTP integration** for automatic OTP generation
- **Secure credential management** via environment variables
- **Automatic token refresh** capabilities

### 📈 Trade Monitoring
- **Real-time trade detection** from completed orders
- **Telegram notifications** for each trade
- **Trade statistics** and logging
- **Duplicate prevention** with order tracking

### 🔒 Security Features
- **No hardcoded credentials** - all loaded from environment variables
- **Secure credential validation** before execution
- **Encrypted config storage** for generated tokens
- **Chrome security options** to avoid detection

## 📁 File Location

```
utils/automated_token_generator.py
```

## ⚙️ Setup Instructions

### 1. Install Additional Dependencies

```bash
pip install selenium webdriver-manager pyotp
```

Or install all dependencies:
```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

Create or update your `.env` file with the following variables:

```bash
# Zerodha Credentials for Automated Token Generation
AUTOMATED_USER_ID=your_zerodha_user_id
AUTOMATED_PASSWORD=your_zerodha_password
AUTOMATED_API_KEY=your_zerodha_api_key
AUTOMATED_API_SECRET=your_zerodha_api_secret
AUTOMATED_AUTH_SECRET=your_zerodha_auth_secret

# Telegram Bot Credentials (Optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

### 3. Install Chrome Browser

The script requires Chrome browser to be installed on your system:
- **Windows**: Download from [Chrome website](https://www.google.com/chrome/)
- **macOS**: Download from [Chrome website](https://www.google.com/chrome/)
- **Linux**: Install via package manager or download from Chrome website

## 🎯 Usage

### Basic Usage

```bash
python utils/automated_token_generator.py
```

### What It Does

1. **Token Generation**:
   - Opens Chrome browser automatically
   - Navigates to Zerodha login page
   - Enters your credentials
   - Generates OTP using your auth secret
   - Completes login process
   - Extracts and generates access token

2. **Trade Monitoring**:
   - Monitors your orders every 15 seconds
   - Detects completed trades
   - Sends Telegram notifications
   - Logs trade statistics

3. **Notifications**:
   - Sends startup notification
   - Notifies for each completed trade
   - Sends stop notification when closed

## 📱 Telegram Setup (Optional)

### 1. Create Telegram Bot

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Save the bot token

### 2. Get Your Chat ID

1. Message your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Find your chat ID in the response
4. Add both to your `.env` file

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AUTOMATED_USER_ID` | Your Zerodha user ID | Yes |
| `AUTOMATED_PASSWORD` | Your Zerodha password | Yes |
| `AUTOMATED_API_KEY` | Your Zerodha API key | Yes |
| `AUTOMATED_API_SECRET` | Your Zerodha API secret | Yes |
| `AUTOMATED_AUTH_SECRET` | Your Zerodha auth secret for TOTP | Yes |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | No |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | No |

### Chrome Options

The script uses these Chrome options for security:
- `--no-sandbox`: Required for some environments
- `--disable-dev-shm-usage`: Prevents crashes
- `--disable-blink-features=AutomationControlled`: Avoids detection
- `excludeSwitches`: Removes automation indicators

## 📊 Output Files

### Generated Files

- **`automated_config.json`**: Contains generated access token and configuration
- **`copy_trader.log`**: System logs and trade information

### Example Output

```json
{
    "kite": {
        "api_key": "your_api_key",
        "access_token": "generated_access_token"
    },
    "telegram": {
        "bot_token": "your_bot_token",
        "chat_id": "your_chat_id"
    },
    "generated_at": "2024-01-01T10:30:00"
}
```

## 🚨 Important Notes

### Security Considerations

- **Never commit** your `.env` file to version control
- **Keep credentials secure** and don't share them
- **Use strong passwords** for your Zerodha account
- **Enable 2FA** on your Zerodha account

### System Requirements

- **Chrome Browser**: Must be installed and updated
- **Stable Internet**: Required for automation and API calls
- **Python 3.7+**: Required for all dependencies
- **Sufficient RAM**: Chrome automation requires memory

### Troubleshooting

#### Common Issues

1. **"Chrome not found"**:
   - Install Chrome browser
   - Update Chrome to latest version

2. **"Credentials missing"**:
   - Check your `.env` file
   - Ensure all required variables are set

3. **"Login failed"**:
   - Verify your credentials
   - Check if 2FA is enabled
   - Ensure auth secret is correct

4. **"Token generation failed"**:
   - Check internet connection
   - Verify API credentials
   - Try running again

#### Debug Mode

Enable debug logging by modifying the script:

```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

## 🔄 Integration with Main System

### Using Generated Token

The generated token can be used with the main copy trading system:

1. **Run automated generator**:
   ```bash
   python utils/automated_token_generator.py
   ```

2. **Use generated token**:
   ```bash
   # The token is saved in automated_config.json
   # You can copy it to your .env file as MASTER_ACCESS_TOKEN
   ```

3. **Start main system**:
   ```bash
   python run.py
   ```

### Daily Workflow

```bash
# Morning: Generate fresh token
python utils/automated_token_generator.py

# Start main trading system
python run.py
```

## 📈 Performance

### Monitoring Frequency

- **Trade checks**: Every 15 seconds
- **Memory cleanup**: After 50 processed orders
- **Token refresh**: Manual (run script again)

### Resource Usage

- **Chrome memory**: ~100-200MB during automation
- **Python memory**: ~50-100MB for monitoring
- **Network**: Minimal after token generation

## 🆘 Support

### Getting Help

1. **Check logs**: Look at `copy_trader.log` for errors
2. **Verify credentials**: Ensure all environment variables are set
3. **Test Chrome**: Make sure Chrome works manually
4. **Check internet**: Ensure stable connection

### Common Solutions

- **Restart Chrome**: Close all Chrome instances and try again
- **Update dependencies**: `pip install --upgrade -r requirements.txt`
- **Clear cache**: Delete `automated_config.json` and try again
- **Check Zerodha**: Ensure your account is active and API access is enabled

---

**⚠️ IMPORTANT**: This script automates browser interactions. Use responsibly and ensure you comply with Zerodha's terms of service.

**🎯 TIP**: Test the script during off-market hours first to ensure everything works correctly.
