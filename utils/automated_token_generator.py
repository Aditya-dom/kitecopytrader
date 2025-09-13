#!/usr/bin/env python3
"""
Automated Token Generator and Trade Monitor
==========================================

This script provides automated access token generation using Selenium
and real-time trade monitoring with Telegram notifications.

Features:
- Automated token generation using Selenium WebDriver
- Real-time trade monitoring
- Telegram notifications for completed trades
- Secure credential management via environment variables
- Trade logging and statistics

Security:
- All credentials loaded from environment variables
- No hardcoded secrets in the code
- Secure credential validation
"""

import os
import time
import urllib.parse
import requests
import pyotp
import json
import logging
import hashlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from kiteconnect import KiteConnect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutomatedKiteSystem:
    def __init__(self):
        """Initialize automated kite system with secure credential loading"""
        # Load credentials from environment variables
        self.USER_ID = os.getenv('AUTOMATED_USER_ID', '')
        self.PASSWORD = os.getenv('AUTOMATED_PASSWORD', '')
        self.API_KEY = os.getenv('AUTOMATED_API_KEY', '')
        self.API_SECRET = os.getenv('AUTOMATED_API_SECRET', '')
        self.AUTH_SECRET = os.getenv('AUTOMATED_AUTH_SECRET', '')
        
        # Telegram credentials
        self.TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
        
        # System state
        self.driver = None
        self.kite = None
        self.processed_orders = set()
        self.trade_count = 0
        
        # Validate credentials
        self._validate_credentials()
        
        logger.info("🎯 Automated Kite System Initialized")
    
    def _validate_credentials(self):
        """Validate that all required credentials are provided"""
        required_credentials = {
            'AUTOMATED_USER_ID': self.USER_ID,
            'AUTOMATED_PASSWORD': self.PASSWORD,
            'AUTOMATED_API_KEY': self.API_KEY,
            'AUTOMATED_API_SECRET': self.API_SECRET,
            'AUTOMATED_AUTH_SECRET': self.AUTH_SECRET,
            'TELEGRAM_BOT_TOKEN': self.TELEGRAM_TOKEN,
            'TELEGRAM_CHAT_ID': self.TELEGRAM_CHAT_ID
        }
        
        missing_credentials = [key for key, value in required_credentials.items() if not value.strip()]
        
        if missing_credentials:
            logger.error(f"Missing required credentials: {', '.join(missing_credentials)}")
            print("\n❌ MISSING CREDENTIALS!")
            print("Please set the following environment variables in your .env file:")
            for cred in missing_credentials:
                print(f"  - {cred}")
            print("\nExample .env entries:")
            print("AUTOMATED_USER_ID=your_user_id")
            print("AUTOMATED_PASSWORD=your_password")
            print("AUTOMATED_API_KEY=your_api_key")
            print("AUTOMATED_API_SECRET=your_api_secret")
            print("AUTOMATED_AUTH_SECRET=your_auth_secret")
            print("TELEGRAM_BOT_TOKEN=your_telegram_bot_token")
            print("TELEGRAM_CHAT_ID=your_telegram_chat_id")
            raise ValueError("Missing required credentials")
    
    def automated_token_generation(self):
        """Generate access token using automated Selenium method"""
        try:
            print("🤖 STEP 1: AUTOMATED TOKEN GENERATION")
            print("-" * 40)
            
            # Create TOTP
            totp = pyotp.TOTP(self.AUTH_SECRET)
            otp = totp.now()
            remaining = 30 - (int(time.time()) % 30)
            
            print(f"🔑 Generated OTP: {otp} (expires in {remaining}s)")
            
            # Setup Chrome with security options
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Navigate and login
            login_url = f"https://kite.zerodha.com/connect/login?api_key={self.API_KEY}&v=3"
            print(f"🌐 Opening: {login_url}")
            
            self.driver.get(login_url)
            wait = WebDriverWait(self.driver, 15)
            
            # Enter credentials
            print("📝 Entering User ID...")
            userid_box = wait.until(EC.presence_of_element_located((By.ID, "userid")))
            userid_box.clear()
            userid_box.send_keys(self.USER_ID)
            userid_box.send_keys(Keys.RETURN)
            
            print("🔒 Entering Password...")
            password_box = wait.until(EC.presence_of_element_located((By.ID, "password")))
            password_box.clear()
            password_box.send_keys(self.PASSWORD)
            password_box.send_keys(Keys.RETURN)
            
            print("🔐 Entering OTP...")
            otp_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.twofa-form input[type='number']")))
            otp_box.clear()
            otp_box.send_keys(otp)
            otp_box.send_keys(Keys.RETURN)
            
            time.sleep(5)
            
            # Extract token
            redirect_url = self.driver.current_url
            print(f"📍 Redirect URL: {redirect_url}")
            
            parsed = urllib.parse.urlparse(redirect_url)
            params = urllib.parse.parse_qs(parsed.query)
            request_token = params.get("request_token", [""])[0]
            
            if not request_token:
                print("❌ Failed to get request token")
                return None
            
            print(f"✅ Request Token: {request_token}")
            
            # Generate access token
            self.kite = KiteConnect(api_key=self.API_KEY)
            data_kite = self.kite.generate_session(request_token, api_secret=self.API_SECRET)
            access_token = data_kite["access_token"]
            
            print(f"✅ Access Token: {access_token[:30]}...")
            
            # Save config securely
            config = {
                "kite": {
                    "api_key": self.API_KEY,
                    "access_token": access_token
                },
                "telegram": {
                    "bot_token": self.TELEGRAM_TOKEN,
                    "chat_id": self.TELEGRAM_CHAT_ID
                },
                "generated_at": datetime.now().isoformat()
            }
            
            with open('automated_config.json', 'w') as f:
                json.dump(config, f, indent=4)
            
            print("✅ Config saved to automated_config.json")
            
            return access_token
            
        except Exception as e:
            logger.error(f"Token generation failed: {e}")
            print(f"❌ Token generation failed: {e}")
            return None
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def send_trade_notification(self, message):
        """Send trade notification to Telegram"""
        try:
            if not self.TELEGRAM_TOKEN or not self.TELEGRAM_CHAT_ID:
                print("⚠️ Telegram credentials not configured")
                return False
            
            url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
            payload = {
                "chat_id": self.TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, data=payload, timeout=10)
            if response.status_code == 200:
                print("✅ Telegram notification sent")
                return True
            else:
                print(f"⚠️ Telegram error: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Notification error: {e}")
            print(f"❌ Notification error: {e}")
            return False
    
    def format_trade_message(self, order):
        """Format trade message for Telegram"""
        try:
            symbol = order.get('tradingsymbol', 'N/A')
            transaction_type = order.get('transaction_type', 'N/A')
            quantity = order.get('quantity', 0)
            price = order.get('price', 0) or order.get('average_price', 0)
            
            emoji = "🟢" if transaction_type == "BUY" else "🔴"
            total = float(quantity) * float(price) if price else 0
            current_time = datetime.now().strftime("%H:%M:%S")
            
            self.trade_count += 1
            
            message = f"""{emoji} <b>{transaction_type}</b> - <code>{symbol}</code>

📊 <b>Qty:</b> {quantity:,} | <b>Price:</b> ₹{price:,.2f}
💰 <b>Total:</b> ₹{total:,.2f}
🕐 <b>Time:</b> {current_time}

Today: {self.trade_count} trades | Happy Trading! 📈"""
            
            return message.strip()
            
        except Exception as e:
            logger.error(f"Message format error: {e}")
            return f"Trade Alert: {order.get('tradingsymbol', 'N/A')} - {order.get('transaction_type', 'N/A')}"
    
    def generate_order_id(self, order):
        """Generate unique ID for order tracking"""
        data = f"{order.get('order_id')}-{order.get('status')}-{order.get('tradingsymbol')}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def monitor_trades(self):
        """Monitor trades and send notifications"""
        try:
            if not self.kite:
                print("❌ Kite client not initialized")
                return
                
            orders = self.kite.orders()
            
            for order in orders:
                order_unique_id = self.generate_order_id(order)
                status = order.get('status', '').upper()
                
                if (status in ['COMPLETE', 'EXECUTED'] and 
                    order_unique_id not in self.processed_orders):
                    
                    message = self.format_trade_message(order)
                    success = self.send_trade_notification(message)
                    
                    if success:
                        self.processed_orders.add(order_unique_id)
                        print(f"✅ Logged: {order.get('tradingsymbol')} - {order.get('transaction_type')}")
                    else:
                        print(f"❌ Failed to notify: {order.get('order_id')}")
            
            # Keep memory clean
            if len(self.processed_orders) > 50:
                self.processed_orders = set(list(self.processed_orders)[-25:])
                
        except Exception as e:
            logger.error(f"Trade monitoring error: {e}")
            print(f"❌ Trade monitoring error: {e}")
    
    def run_automated_system(self):
        """Run complete automated system"""
        
        print("🎯 AUTOMATED KITE SYSTEM")
        print("="*50)
        print("🚀 Step 1: Auto-generate access token")
        print("📈 Step 2: Start trade monitoring")
        print("📱 Step 3: Send Telegram notifications")
        print("="*50)
        print()
        
        # Step 1: Generate access token
        access_token = self.automated_token_generation()
        if not access_token:
            print("❌ FAILED: Could not generate access token")
            return False
        
        print("\n" + "="*50)
        print("🎉 TOKEN GENERATION SUCCESSFUL!")
        print("="*50)
        print(f"✅ Access Token: {access_token[:30]}...")
        print("✅ Config saved")
        print()
        
        # Step 2: Start trade monitoring
        print("📈 STEP 2: STARTING TRADE MONITORING")
        print("-" * 40)
        
        if not self.TELEGRAM_TOKEN or not self.TELEGRAM_CHAT_ID:
            print("⚠️ IMPORTANT: Configure Telegram credentials to receive notifications")
            print("💡 Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID to your .env file")
        
        # Send startup notification
        startup_msg = f"🚀 <b>Automated Kite System Started</b>\n\n⏰ Time: {datetime.now().strftime('%H:%M:%S')}\n📊 Ready to monitor trades!"
        self.send_trade_notification(startup_msg)
        
        print("✅ Trade monitoring active")
        print("💡 Press Ctrl+C to stop")
        print()
        
        try:
            while True:
                self.monitor_trades()
                time.sleep(15)  # Check every 15 seconds
                
        except KeyboardInterrupt:
            print("\n🛑 Trade monitoring stopped")
            
            # Send stop notification
            stop_msg = f"🛑 <b>Automated System Stopped</b>\n\nSession trades: {self.trade_count}\nThanks for using Automated Kite System! 👋"
            self.send_trade_notification(stop_msg)
            
            return True

def main():
    """Main function"""
    print("🎯 Starting Automated Kite System...")
    print("💡 Automated token generation + Trade monitoring + Notifications!")
    print()
    
    # Prerequisites check
    print("📋 PREREQUISITES:")
    print("1. Chrome browser installed")
    print("2. All credentials set in .env file")
    print("3. Stable internet connection")
    print("4. Telegram bot configured (optional)")
    print()
    
    proceed = input("Ready to start? (y/n): ").lower().strip()
    if proceed != 'y':
        print("👋 Setup cancelled")
        return
    
    try:
        system = AutomatedKiteSystem()
        success = system.run_automated_system()
        
        if success:
            print("\n🎉 AUTOMATED SYSTEM COMPLETED!")
            print("\n📋 What happened:")
            print("✅ Access token generated automatically")
            print("✅ Trade monitoring was active")
            print("✅ Notifications sent to Telegram")
            print("\n💡 Run again anytime with: python utils/automated_token_generator.py")
        else:
            print("\n❌ SYSTEM FAILED!")
            print("💡 Check error messages above")
            
    except Exception as e:
        logger.error(f"System error: {e}")
        print(f"\n❌ SYSTEM ERROR: {e}")
        print("💡 Check your credentials and try again")

if __name__ == "__main__":
    main()
