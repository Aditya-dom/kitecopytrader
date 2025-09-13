# config.py
import os
import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Load environment variables from .env file
load_dotenv()

@dataclass
class AccountConfig:
    """Configuration for a trading account with multi-segment support"""
    api_key: str
    api_secret: str
    access_token: str
    user_id: str
    multiplier: float = 1.0
    max_position_size: int = 1000
    enabled: bool = True
    # Multi-segment trading configuration
    enabled_segments: List[str] = None  # List of enabled segments
    segment_multipliers: Dict[str, float] = None  # Different multipliers per segment
    segment_limits: Dict[str, int] = None  # Different limits per segment
    
    def __post_init__(self):
        # Default enabled segments if not specified
        if self.enabled_segments is None:
            self.enabled_segments = [
                'NSE',      # NSE Equity
                'BSE',      # BSE Equity  
                'NFO',      # NSE Futures & Options
                'MCX',      # Commodities
                'BFO',      # BSE Futures & Options
                'CDS'       # Currency Derivatives
            ]
        
        # Default segment multipliers (same as main multiplier if not specified)
        if self.segment_multipliers is None:
            self.segment_multipliers = {
                'NSE': self.multiplier,
                'BSE': self.multiplier,
                'NFO': self.multiplier,
                'MCX': self.multiplier,
                'BFO': self.multiplier,
                'CDS': self.multiplier
            }
        
        # Default segment limits with appropriate defaults for each segment
        if self.segment_limits is None:
            self.segment_limits = {
                'NSE': self.max_position_size,       # Equity: Full limit
                'BSE': self.max_position_size,       # BSE Equity: Full limit
                'NFO': self.max_position_size // 2,  # F&O: Smaller lots due to leverage
                'MCX': self.max_position_size // 5,  # Commodities: Much smaller due to high value
                'BFO': self.max_position_size // 2,  # BSE F&O: Smaller lots
                'CDS': self.max_position_size        # Currency: Full limit
            }

class SecureConfigManager:
    """
    Secure configuration manager for API credentials and system settings.
    
    Security Features:
    - Environment variable support
    - Optional encryption for sensitive data
    - Secure credential validation
    - Configuration file with .gitignore protection
    """
    
    def __init__(self, config_file: str = "config.json", encryption_key: Optional[str] = None):
        self.config_file = config_file
        self.encryption_key = encryption_key
        self.cipher = None
        
        if encryption_key:
            self.cipher = Fernet(encryption_key.encode())
            
        # System configuration
        self.system_config = {
            'check_interval': int(os.getenv('CHECK_INTERVAL', '1')),
            'max_retries': int(os.getenv('MAX_RETRIES', '3')),
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'paper_trading': os.getenv('PAPER_TRADING', 'True').lower() == 'true',
            'max_daily_trades': int(os.getenv('MAX_DAILY_TRADES', '100')),
            'risk_management_enabled': os.getenv('RISK_MANAGEMENT', 'True').lower() == 'true'
        }
        
    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data if cipher is available"""
        if self.cipher:
            return self.cipher.encrypt(data.encode()).decode()
        return data
    
    def _decrypt_data(self, data: str) -> str:
        """Decrypt sensitive data if cipher is available"""
        if self.cipher:
            try:
                return self.cipher.decrypt(data.encode()).decode()
            except:
                return data  # Return as-is if decryption fails
        return data
    
    def load_master_config(self) -> AccountConfig:
        """Load master account configuration from environment variables"""
        return AccountConfig(
            api_key=os.getenv('MASTER_API_KEY', ''),
            api_secret=self._decrypt_data(os.getenv('MASTER_API_SECRET', '')),
            access_token=self._decrypt_data(os.getenv('MASTER_ACCESS_TOKEN', '')),
            user_id=os.getenv('MASTER_USER_ID', ''),
            multiplier=1.0  # Master always has 1.0 multiplier
        )
    
    def load_follower_configs(self) -> List[AccountConfig]:
        """Load follower account configurations with segment-specific settings"""
        followers = []
        
        # Try to load from environment variables first
        follower_count = int(os.getenv('FOLLOWER_COUNT', '0'))
        
        for i in range(1, follower_count + 1):
            # Load basic configuration
            follower = AccountConfig(
                api_key=os.getenv(f'FOLLOWER_{i}_API_KEY', ''),
                api_secret=self._decrypt_data(os.getenv(f'FOLLOWER_{i}_API_SECRET', '')),
                access_token=self._decrypt_data(os.getenv(f'FOLLOWER_{i}_ACCESS_TOKEN', '')),
                user_id=os.getenv(f'FOLLOWER_{i}_USER_ID', ''),
                multiplier=float(os.getenv(f'FOLLOWER_{i}_MULTIPLIER', '1.0')),
                max_position_size=int(os.getenv(f'FOLLOWER_{i}_MAX_POSITION', '1000')),
                enabled=os.getenv(f'FOLLOWER_{i}_ENABLED', 'True').lower() == 'true'
            )
            
            # Load segment-specific settings if available
            enabled_segments_str = os.getenv(f'FOLLOWER_{i}_ENABLED_SEGMENTS', '')
            if enabled_segments_str:
                follower.enabled_segments = [seg.strip() for seg in enabled_segments_str.split(',')]
            
            # Load segment-specific multipliers
            segment_multipliers = {}
            segment_limits = {}
            
            for segment in ['NSE', 'BSE', 'NFO', 'MCX', 'BFO', 'CDS']:
                # Load multiplier for this segment
                multiplier_key = f'FOLLOWER_{i}_{segment}_MULTIPLIER'
                if os.getenv(multiplier_key):
                    segment_multipliers[segment] = float(os.getenv(multiplier_key))
                
                # Load limit for this segment
                limit_key = f'FOLLOWER_{i}_{segment}_LIMIT'
                if os.getenv(limit_key):
                    segment_limits[segment] = int(os.getenv(limit_key))
            
            # Apply segment-specific settings if any were found
            if segment_multipliers:
                follower.segment_multipliers = segment_multipliers
            if segment_limits:
                follower.segment_limits = segment_limits
            
            if self._validate_account_config(follower):
                followers.append(follower)
                logging.info(f"Loaded follower {i} with segments: {follower.enabled_segments}")
        
        # Try to load from config file if no environment variables found
        if not followers and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    
                for follower_data in config_data.get('followers', []):
                    follower = AccountConfig(**follower_data)
                    if self._validate_account_config(follower):
                        followers.append(follower)
            except Exception as e:
                logging.error(f"Error loading config file: {e}")
        
        return followers
    
    def _validate_account_config(self, config: AccountConfig) -> bool:
        """Validate account configuration"""
        required_fields = [config.api_key, config.api_secret, config.access_token, config.user_id]
        return all(field.strip() for field in required_fields)
    
    def get_system_config(self) -> Dict:
        """Get system configuration"""
        return self.system_config.copy()
    
    def create_sample_config_file(self):
        """Create a sample configuration file"""
        sample_config = {
            "followers": [
                {
                    "api_key": "YOUR_FOLLOWER_1_API_KEY",
                    "api_secret": "YOUR_FOLLOWER_1_API_SECRET", 
                    "access_token": "YOUR_FOLLOWER_1_ACCESS_TOKEN",
                    "user_id": "YOUR_FOLLOWER_1_USER_ID",
                    "multiplier": 1.0,
                    "max_position_size": 1000,
                    "enabled": True
                }
            ]
        }
        
        with open('config.json.sample', 'w') as f:
            json.dump(sample_config, f, indent=2)
        
        print("Sample configuration file created: config.json.sample")
        print("Copy to config.json and update with your credentials")

# Setup logging configuration
def setup_logging(log_level: str = "INFO"):
    """Setup structured logging"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('copy_trader.log'),
            logging.StreamHandler()
        ]
    )
