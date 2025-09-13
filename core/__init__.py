"""
Core Trading System Module
=========================

Contains the main trading system components:
- main.py: System orchestrator and launcher
- master_client.py: Master account monitoring
- follower_client.py: Trade replication engine
- notifications.py: Multi-channel notification system
- config.py: Configuration management
"""

from .main import CopyTradingSystem
from .master_client import MasterAccountClient
from .follower_client import FollowerAccountClient
from .notifications import NotificationManager, NotificationConfig
from .config import SecureConfigManager, AccountConfig

__all__ = [
    'CopyTradingSystem',
    'MasterAccountClient', 
    'FollowerAccountClient',
    'NotificationManager',
    'NotificationConfig',
    'SecureConfigManager',
    'AccountConfig'
]
