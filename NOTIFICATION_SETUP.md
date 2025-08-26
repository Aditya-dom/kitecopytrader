# Notification Setup Guide
# ========================

# QUICK SETUP FOR TELEGRAM (EASIEST!)

## Step 1: Create Telegram Bot
1. Open Telegram and search for @BotFather
2. Send /newbot command
3. Choose a name for your bot (e.g., "My Copy Trading Bot")
4. Choose a username (e.g., "mycopytrading_bot")
5. Copy the bot token (looks like: 123456789:ABCdefGhIjKlMnOpQrStUvWxYz)

## Step 2: Get Your Chat ID
1. Send a message to your new bot
2. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
3. Look for your chat ID in the response (it's a number like: 123456789)

## Step 3: Update .env file
```
TELEGRAM_ENABLED=True
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIjKlMnOpQrStUvWxYz
TELEGRAM_CHAT_ID=123456789
```

# 📱 WHATSAPP SETUP (via Twilio)

## Step 1: Create Twilio Account
1. Go to https://www.twilio.com/
2. Sign up for free account
3. Verify your phone number
4. Go to Console Dashboard

## Step 2: Get WhatsApp Sandbox
1. In Twilio Console, go to Messaging > Try it out > Send a WhatsApp message
2. Follow the instructions to join the sandbox
3. Send the join code to the sandbox number

## Step 3: Get Credentials
1. Account SID: Found on your Dashboard
2. Auth Token: Found on your Dashboard (click to reveal)
3. WhatsApp From: whatsapp:+14155238886 (Twilio sandbox number)
4. WhatsApp To: whatsapp:+91XXXXXXXXXX (your number with country code)

## Step 4: Update .env file
```
WHATSAPP_ENABLED=True
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
WHATSAPP_TO=whatsapp:+919876543210
```

# 📧 EMAIL SETUP (Gmail Example)

## Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Enable 2-Factor Authentication

## Step 2: Generate App Password
1. Go to Google Account > Security > 2-Step Verification
2. Scroll down to "App passwords"
3. Generate password for "Mail"
4. Copy the 16-character password

## Step 3: Update .env file
```
EMAIL_ENABLED=True
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
EMAIL_TO=notifications@yourcompany.com
```

# 🔔 WHAT YOU'LL RECEIVE

## Real-Time Trade Notifications
```
**TRADE EXECUTED**

**Symbol:** RELIANCE
**Exchange:** NSE
**Action:** BUY
**Quantity:** 100
**Price:** ₹2,500.50
**Value:** ₹2,50,050.00
**Time:** 14:35:22

**FOLLOWER RESULTS:**
SUCCESS: USER123: 100 shares
SUCCESS: USER456: 50 shares
ERROR: USER789: FAILED - Insufficient funds

**Summary:** 2 successful, 1 failed
```

## System Alerts
```
**SYSTEM WARNING**

**Type:** Partial Replication Failure
**Time:** 2024-01-20 14:35:25

**Details:**
Trade for RELIANCE failed on 1 follower account(s). 
Check logs for details.

🔧 **Action Required:** Please check the system logs
```

## Daily Summary
```
📅 **DAILY COPY TRADING SUMMARY**

**Date:** 2024-01-20

**Trading Statistics:**
• Total Trades: 15
• Successful Copies: 28
• Failed Copies: 2
• Success Rate: 93.3%

**Segment Breakdown:**
• NSE: 8 trades
• MCX: 4 trades
• NFO: 3 trades

👥 **Follower Performance:**
• USER123: 15/15 (100.0%)
• USER456: 13/15 (86.7%)

**System Uptime:** 8:45:32
```

# RECOMMENDATIONS

## For Best Experience:
1. **Start with Telegram** - Easiest to setup, free, reliable
2. **Add WhatsApp** - For critical alerts when you're not on Telegram
3. **Email for Records** - Keep email logs for audit trail
4. **Test First** - Send test notifications before going live

## Notification Levels:
- **INFO**: System startup, daily summaries
- **WARNING**: Partial failures, trading blocks
- **ERROR**: Critical system errors, connection issues
- **All successful trades** get notified regardless of level

# ⚡ QUICK TEST

Once configured, test your notifications:

```bash
python3 -c "
from notifications import load_notification_config, NotificationManager
config = load_notification_config()
nm = NotificationManager(config)
nm.send_system_alert('Test', 'Notification system working!', 'INFO')
print('Test notification sent!')
"
```

# SECURITY NOTES

1. **Keep bot tokens secure** - Don't share or commit to git
2. **Use app passwords** - Don't use your main email password  
3. **Monitor usage** - Check for unexpected notifications
4. **Revoke if needed** - You can always disable/revoke access

# PRO TIPS

1. **Create separate Telegram group** for trading notifications
2. **Use Telegram's notification settings** to customize alerts
3. **Set up email filters** to organize trading notifications
4. **Test during paper trading** to fine-tune notification preferences
