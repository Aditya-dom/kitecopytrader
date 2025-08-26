# notifications.py
"""
Notification System for Zerodha Copy Trading
==========================================

Supports multiple notification channels:
- WhatsApp (via Twilio WhatsApp API)
- Telegram (via Telegram Bot API)
- Email (via SMTP)
- Discord (via Webhooks)
"""

import os
import logging
import asyncio
import aiohttp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
import requests
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class NotificationConfig:
    """Configuration for notification channels"""
    # WhatsApp (Twilio)
    whatsapp_enabled: bool = False
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_whatsapp_from: str = ""  # e.g., "whatsapp:+14155238886"
    whatsapp_to: str = ""  # e.g., "whatsapp:+919876543210"
    
    # Telegram
    telegram_enabled: bool = False
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    # Email
    email_enabled: bool = False
    smtp_server: str = ""
    smtp_port: int = 587
    email_user: str = ""
    email_password: str = ""
    email_to: str = ""
    
    # Discord
    discord_enabled: bool = False
    discord_webhook_url: str = ""

class NotificationManager:
    """Manages all notification channels for copy trading events"""
    
    def __init__(self, config: NotificationConfig):
        self.config = config
        self.session = None
        
        # Initialize Twilio client if WhatsApp is enabled
        self.twilio_client = None
        if self.config.whatsapp_enabled:
            try:
                from twilio.rest import Client
                self.twilio_client = Client(
                    self.config.twilio_account_sid, 
                    self.config.twilio_auth_token
                )
                logger.info("Twilio WhatsApp client initialized")
            except ImportError:
                logger.error("Twilio library not installed. Run: pip install twilio")
                self.config.whatsapp_enabled = False
            except Exception as e:
                logger.error(f"Failed to initialize Twilio: {e}")
                self.config.whatsapp_enabled = False
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    def send_trade_notification(self, trade_data: Dict[str, Any], results: List[Dict[str, Any]]):
        """Send notification when a trade is executed"""
        try:
            # Format the message
            message = self._format_trade_message(trade_data, results)
            
            # Send to all enabled channels
            if self.config.whatsapp_enabled:
                self._send_whatsapp(message)
            
            if self.config.telegram_enabled:
                asyncio.create_task(self._send_telegram(message))
            
            if self.config.email_enabled:
                self._send_email("Copy Trading Alert - Trade Executed", message)
            
            if self.config.discord_enabled:
                asyncio.create_task(self._send_discord(message))
                
        except Exception as e:
            logger.error(f"Error sending trade notification: {e}")
    
    def send_system_alert(self, alert_type: str, message: str, severity: str = "INFO"):
        """Send system alerts (errors, connections, etc.)"""
        try:
            # Format system alert
            alert_message = self._format_system_alert(alert_type, message, severity)
            
            # Send to all enabled channels (only for WARNING/ERROR)
            if severity in ["WARNING", "ERROR"]:
                if self.config.whatsapp_enabled:
                    self._send_whatsapp(alert_message)
                
                if self.config.telegram_enabled:
                    asyncio.create_task(self._send_telegram(alert_message))
                
                if self.config.discord_enabled:
                    asyncio.create_task(self._send_discord(alert_message))
            
            # Always send to email for logging
            if self.config.email_enabled:
                self._send_email(f"Copy Trading {severity} - {alert_type}", alert_message)
                
        except Exception as e:
            logger.error(f"Error sending system alert: {e}")
    
    def send_daily_summary(self, summary_data: Dict[str, Any]):
        """Send daily trading summary"""
        try:
            message = self._format_daily_summary(summary_data)
            
            # Send summary to all channels
            if self.config.whatsapp_enabled:
                self._send_whatsapp(message)
            
            if self.config.telegram_enabled:
                asyncio.create_task(self._send_telegram(message))
            
            if self.config.email_enabled:
                self._send_email("Daily Copy Trading Summary", message)
            
            if self.config.discord_enabled:
                asyncio.create_task(self._send_discord(message))
                
        except Exception as e:
            logger.error(f"Error sending daily summary: {e}")
    
    def _format_trade_message(self, trade_data: Dict[str, Any], results: List[Dict[str, Any]]) -> str:
        """Format trade execution message"""
        exchange = trade_data.get('exchange', 'NSE')
        symbol = trade_data.get('tradingsymbol', 'UNKNOWN')
        quantity = trade_data.get('quantity', 0)
        transaction_type = trade_data.get('transaction_type', 'UNKNOWN')
        price = trade_data.get('price', 0)
        
        # Emoji based on segment
        segment_emoji = {
            'NSE': 'NSE', 'BSE': 'BSE', 'NFO': 'NFO', 
            'MCX': 'MCX', 'BFO': 'BFO', 'CDS': 'CDS'
        }.get(exchange, 'KITE')
        
        # Transaction emoji
        action_emoji = '🟢' if transaction_type == 'BUY' else '🔴'
        
        message = f"{segment_emoji} **TRADE EXECUTED** {action_emoji}\n\n"
        message += f"**Symbol:** {symbol}\n"
        message += f"**Exchange:** {exchange}\n"
        message += f"**Action:** {transaction_type}\n"
        message += f"**Quantity:** {quantity:,}\n"
        message += f"**Price:** ₹{price:.2f}\n"
        message += f"**Value:** ₹{(quantity * price):,.2f}\n"
        message += f"**Time:** {datetime.now().strftime('%H:%M:%S')}\n\n"
        
        # Follower results
        message += "**FOLLOWER RESULTS:**\n"
        successful = 0
        failed = 0
        
        for result in results:
            user_id = result.get('user_id', 'Unknown')
            success = result.get('success', False)
            replicated_qty = result.get('replicated_quantity', 0)
            error = result.get('error', '')
            
            if success:
                message += f"SUCCESS: {user_id}: {replicated_qty:,} shares\n"
                successful += 1
            else:
                message += f"ERROR: {user_id}: FAILED - {error[:50]}...\n"
                failed += 1
        
        message += f"\n**Summary:** {successful} successful, {failed} failed"
        
        return message
    
    def _format_system_alert(self, alert_type: str, message: str, severity: str) -> str:
        """Format system alert message"""
        severity_emoji = {
            'INFO': 'INFO',
            'WARNING': 'WARNING', 
            'ERROR': 'ERROR',
            'CRITICAL': 'CRITICAL'
        }.get(severity, 'INFO')
        
        alert_message = f"{severity_emoji} **SYSTEM {severity}** {severity_emoji}\n\n"
        alert_message += f"**Type:** {alert_type}\n"
        alert_message += f"**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        alert_message += f"**Details:**\n{message}\n"
        
        if severity in ['ERROR', 'CRITICAL']:
            alert_message += "\n🔧 **Action Required:** Please check the system logs"
        
        return alert_message
    
    def _format_daily_summary(self, summary_data: Dict[str, Any]) -> str:
        """Format daily summary message"""
        message = "📅 **DAILY COPY TRADING SUMMARY**\n\n"
        message += f"**Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n"
        
        # Trading stats
        total_trades = summary_data.get('total_trades', 0)
        successful_copies = summary_data.get('successful_copies', 0)
        failed_copies = summary_data.get('failed_copies', 0)
        
        message += "**Trading Statistics:**\n"
        message += f"• Total Trades: {total_trades}\n"
        message += f"• Successful Copies: {successful_copies}\n"
        message += f"• Failed Copies: {failed_copies}\n"
        message += f"• Success Rate: {(successful_copies/(total_trades*len(summary_data.get('followers', []))) if total_trades > 0 else 0)*100:.1f}%\n\n"
        
        # Segment breakdown
        if 'segment_breakdown' in summary_data:
            message += "**Segment Breakdown:**\n"
            for segment, count in summary_data['segment_breakdown'].items():
                emoji = {'NSE': 'NSE', 'BSE': 'BSE', 'NFO': 'NFO', 'MCX': 'MCX', 'BFO': 'BFO', 'CDS': 'CDS'}.get(segment, 'UNK')
                message += f"• {emoji} {segment}: {count} trades\n"
            message += "\n"
        
        # Follower performance
        if 'follower_performance' in summary_data:
            message += "👥 **Follower Performance:**\n"
            for follower_id, stats in summary_data['follower_performance'].items():
                success_rate = (stats['successful'] / stats['total'] * 100) if stats['total'] > 0 else 0
                message += f"• {follower_id}: {stats['successful']}/{stats['total']} ({success_rate:.1f}%)\n"
            message += "\n"
        
        # System uptime
        uptime = summary_data.get('uptime', '0:00:00')
        message += f"**System Uptime:** {uptime}\n"
        message += f"**Last Update:** {datetime.now().strftime('%H:%M:%S')}"
        
        return message
    
    def _send_whatsapp(self, message: str):
        """Send WhatsApp message via Twilio"""
        try:
            if not self.twilio_client:
                return
                
            # Send message
            message_instance = self.twilio_client.messages.create(
                body=message,
                from_=self.config.twilio_whatsapp_from,
                to=self.config.whatsapp_to
            )
            
            logger.info(f"WhatsApp message sent: {message_instance.sid}")
            
        except Exception as e:
            logger.error(f"Failed to send WhatsApp message: {e}")
    
    async def _send_telegram(self, message: str):
        """Send Telegram message"""
        try:
            url = f"https://api.telegram.org/bot{self.config.telegram_bot_token}/sendMessage"
            
            payload = {
                'chat_id': self.config.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.post(url, json=payload) as response:
                if response.status == 200:
                    logger.info("Telegram message sent successfully")
                else:
                    logger.error(f"Telegram API error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
    
    def _send_email(self, subject: str, message: str):
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config.email_user
            msg['To'] = self.config.email_to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()
            server.login(self.config.email_user, self.config.email_password)
            text = msg.as_string()
            server.sendmail(self.config.email_user, self.config.email_to, text)
            server.quit()
            
            logger.info("Email sent successfully")
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    
    async def _send_discord(self, message: str):
        """Send Discord webhook message"""
        try:
            payload = {
                'content': message,
                'username': 'Copy Trading Bot'
            }
            
            if not self.session:
                self.session = aiohttp.ClientSession()
            
            async with self.session.post(self.config.discord_webhook_url, json=payload) as response:
                if response.status == 204:
                    logger.info("Discord message sent successfully")
                else:
                    logger.error(f"Discord webhook error: {response.status}")
                    
        except Exception as e:
            logger.error(f"Failed to send Discord message: {e}")

def load_notification_config() -> NotificationConfig:
    """Load notification configuration from environment variables"""
    return NotificationConfig(
        # WhatsApp
        whatsapp_enabled=os.getenv('WHATSAPP_ENABLED', 'False').lower() == 'true',
        twilio_account_sid=os.getenv('TWILIO_ACCOUNT_SID', ''),
        twilio_auth_token=os.getenv('TWILIO_AUTH_TOKEN', ''),
        twilio_whatsapp_from=os.getenv('TWILIO_WHATSAPP_FROM', ''),
        whatsapp_to=os.getenv('WHATSAPP_TO', ''),
        
        # Telegram
        telegram_enabled=os.getenv('TELEGRAM_ENABLED', 'False').lower() == 'true',
        telegram_bot_token=os.getenv('TELEGRAM_BOT_TOKEN', ''),
        telegram_chat_id=os.getenv('TELEGRAM_CHAT_ID', ''),
        
        # Email
        email_enabled=os.getenv('EMAIL_ENABLED', 'False').lower() == 'true',
        smtp_server=os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        smtp_port=int(os.getenv('SMTP_PORT', '587')),
        email_user=os.getenv('EMAIL_USER', ''),
        email_password=os.getenv('EMAIL_PASSWORD', ''),
        email_to=os.getenv('EMAIL_TO', ''),
        
        # Discord
        discord_enabled=os.getenv('DISCORD_ENABLED', 'False').lower() == 'true',
        discord_webhook_url=os.getenv('DISCORD_WEBHOOK_URL', '')
    )

# Quick setup functions for easy integration
class QuickNotifications:
    """Simple notification setup for common use cases"""
    
    @staticmethod
    def setup_telegram(bot_token: str, chat_id: str) -> NotificationManager:
        """Quick Telegram setup"""
        config = NotificationConfig(
            telegram_enabled=True,
            telegram_bot_token=bot_token,
            telegram_chat_id=chat_id
        )
        return NotificationManager(config)
    
    @staticmethod
    def setup_whatsapp(account_sid: str, auth_token: str, from_number: str, to_number: str) -> NotificationManager:
        """Quick WhatsApp setup"""
        config = NotificationConfig(
            whatsapp_enabled=True,
            twilio_account_sid=account_sid,
            twilio_auth_token=auth_token,
            twilio_whatsapp_from=from_number,
            whatsapp_to=to_number
        )
        return NotificationManager(config)
