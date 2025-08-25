# main.py
import logging
import signal
import sys
import time
import threading
from typing import List, Dict, Any
from datetime import datetime, time as dt_time

# Import our modules
from config import SecureConfigManager, setup_logging, AccountConfig
from master_client import MasterAccountClient  
from follower_client import FollowerAccountClient

logger = logging.getLogger(__name__)

class CopyTradingSystem:
    """
    Main copy trading system that coordinates master and follower accounts.
    
    Features:
    - Secure credential management
    - Real-time trade replication
    - Comprehensive error handling and logging
    - System health monitoring
    - Graceful shutdown handling
    """
    
    def __init__(self, config_manager: SecureConfigManager):
        self.config_manager = config_manager
        self.system_config = config_manager.get_system_config()
        
        # Initialize accounts
        self.master_client = None
        self.follower_clients: List[FollowerAccountClient] = []
        
        # System state
        self.is_running = False
        self.start_time = None
        self.total_trades_processed = 0
        self.successful_replications = 0
        self.failed_replications = 0
        
        # Threading
        self.monitor_thread = None
        self.shutdown_event = threading.Event()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self.shutdown()
    
    def initialize_accounts(self) -> bool:
        """Initialize master and follower accounts"""
        try:
            logger.info("Initializing trading accounts...")
            
            # Load master account configuration
            master_config = self.config_manager.load_master_config()
            if not self._validate_account_config(master_config):
                logger.error("Invalid master account configuration")
                return False
            
            # Initialize master client
            self.master_client = MasterAccountClient(
                config=master_config,
                on_trade_callback=self._on_master_trade
            )
            
            # Load follower account configurations
            follower_configs = self.config_manager.load_follower_configs()
            if not follower_configs:
                logger.error("No valid follower accounts configured")
                return False
            
            logger.info(f"Found {len(follower_configs)} follower accounts")
            
            # Initialize follower clients
            for config in follower_configs:
                if config.enabled:
                    follower_client = FollowerAccountClient(config)
                    
                    # Validate connection
                    if follower_client.validate_connection():
                        self.follower_clients.append(follower_client)
                        logger.info(f"Follower account initialized: {config.user_id}")
                    else:
                        logger.error(f"Failed to initialize follower account: {config.user_id}")
                else:
                    logger.info(f"Follower account disabled: {config.user_id}")
            
            if not self.follower_clients:
                logger.error("No valid follower accounts available")
                return False
            
            logger.info(f"Successfully initialized {len(self.follower_clients)} follower accounts")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing accounts: {e}")
            return False
    
    def _validate_account_config(self, config: AccountConfig) -> bool:
        """Validate account configuration"""
        required_fields = [config.api_key, config.api_secret, config.access_token, config.user_id]
        return all(field.strip() for field in required_fields)
    
    def _on_master_trade(self, trade_data: Dict[str, Any]):
        """Handle trades from master account"""
        try:
            logger.info(f"Processing master trade: {trade_data}")
            self.total_trades_processed += 1
            
            # Check if trading is allowed (market hours, system status, etc.)
            if not self._is_trading_allowed():
                logger.warning("Trading is not allowed at this time")
                return
            
            # Replicate trade to all follower accounts
            successful_count = 0
            for follower_client in self.follower_clients:
                try:
                    if follower_client.replicate_trade(trade_data):
                        successful_count += 1
                        logger.info(f"Trade replicated successfully to {follower_client.config.user_id}")
                    else:
                        logger.error(f"Failed to replicate trade to {follower_client.config.user_id}")
                        
                except Exception as e:
                    logger.error(f"Error replicating trade to {follower_client.config.user_id}: {e}")
            
            # Update statistics
            if successful_count == len(self.follower_clients):
                self.successful_replications += 1
                logger.info("Trade replicated successfully to all followers")
            else:
                self.failed_replications += 1
                logger.warning(f"Trade replicated to only {successful_count}/{len(self.follower_clients)} followers")
                
        except Exception as e:
            logger.error(f"Error processing master trade: {e}")
            self.failed_replications += 1
    
    def _is_trading_allowed(self) -> bool:
        """Check if trading is currently allowed"""
        
        # Check if it's paper trading mode
        if self.system_config['paper_trading']:
            logger.info("Paper trading mode - trades will be simulated")
            return False  # Don't actually place trades in paper mode
        
        # Check market hours (9:15 AM to 3:30 PM IST)
        current_time = datetime.now().time()
        market_start = dt_time(9, 15)
        market_end = dt_time(15, 30)
        
        if not (market_start <= current_time <= market_end):
            logger.warning(f"Outside market hours: {current_time}")
            return False
        
        # Check if it's a weekday (Monday=0, Sunday=6)
        current_day = datetime.now().weekday()
        if current_day >= 5:  # Saturday or Sunday
            logger.warning("Market is closed on weekends")
            return False
        
        return True
    
    def start_system(self) -> bool:
        """Start the copy trading system"""
        try:
            logger.info("Starting copy trading system...")
            
            # Initialize accounts if not already done
            if not self.master_client or not self.follower_clients:
                if not self.initialize_accounts():
                    return False
            
            # Start master account monitoring
            if not self.master_client.start_monitoring():
                logger.error("Failed to start master account monitoring")
                return False
            
            # Reset daily statistics for all followers
            for follower_client in self.follower_clients:
                follower_client.reset_daily_stats()
            
            # Start system monitoring thread
            self.is_running = True
            self.start_time = datetime.now()
            
            self.monitor_thread = threading.Thread(target=self._system_monitor, daemon=True)
            self.monitor_thread.start()
            
            logger.info("Copy trading system started successfully")
            logger.info(f"Master account: {self.master_client.config.user_id}")
            logger.info(f"Follower accounts: {len(self.follower_clients)}")
            logger.info(f"Paper trading mode: {self.system_config['paper_trading']}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error starting copy trading system: {e}")
            self.shutdown()
            return False
    
    def _system_monitor(self):
        """Monitor system health and performance"""
        while self.is_running and not self.shutdown_event.is_set():
            try:
                # Log system status every 5 minutes
                if int(time.time()) % 300 == 0:
                    self._log_system_status()
                
                # Check master connection health
                if self.master_client:
                    status = self.master_client.get_connection_status()
                    if not status['connected']:
                        logger.warning("Master account connection lost")
                
                # Sleep for a short interval
                time.sleep(10)
                
            except Exception as e:
                logger.error(f"Error in system monitor: {e}")
                time.sleep(30)
    
    def _log_system_status(self):
        """Log current system status and statistics"""
        uptime = datetime.now() - self.start_time if self.start_time else None
        
        logger.info("=== SYSTEM STATUS ===")
        logger.info(f"Uptime: {uptime}")
        logger.info(f"Total trades processed: {self.total_trades_processed}")
        logger.info(f"Successful replications: {self.successful_replications}")
        logger.info(f"Failed replications: {self.failed_replications}")
        
        # Log master connection status
        if self.master_client:
            master_status = self.master_client.get_connection_status()
            logger.info(f"Master connection: {'Connected' if master_status['connected'] else 'Disconnected'}")
            logger.info(f"Master reconnect count: {master_status['reconnect_count']}")
        
        # Log follower account status
        for i, follower in enumerate(self.follower_clients):
            status = follower.get_account_status()
            logger.info(f"Follower {i+1} ({status['user_id']}): "
                       f"Enabled={status['enabled']}, "
                       f"Daily trades={status['daily_trades_count']}, "
                       f"Multiplier={status['multiplier']}")
        
        logger.info("=== END STATUS ===")
    
    def shutdown(self):
        """Shutdown the copy trading system gracefully"""
        try:
            logger.info("Shutting down copy trading system...")
            
            # Set shutdown flag
            self.is_running = False
            self.shutdown_event.set()
            
            # Stop master account monitoring
            if self.master_client:
                self.master_client.stop_monitoring()
            
            # Wait for monitor thread to finish
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=10)
            
            # Log final statistics
            self._log_system_status()
            
            logger.info("Copy trading system shutdown complete")
            
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    def run(self):
        """Main run loop for the copy trading system"""
        try:
            logger.info("Copy Trading System Starting...")
            
            # Start the system
            if not self.start_system():
                logger.error("Failed to start copy trading system")
                return False
            
            # Keep the main thread alive
            while self.is_running:
                try:
                    time.sleep(1)
                except KeyboardInterrupt:
                    logger.info("Received interrupt signal")
                    break
            
            return True
            
        except Exception as e:
            logger.error(f"Error in main run loop: {e}")
            return False
        finally:
            self.shutdown()

def main():
    """Main entry point"""
    print("=" * 60)
    print("ZERODHA COPY TRADING SYSTEM")
    print("=" * 60)
    print()
    
    # Setup logging
    setup_logging("INFO")
    logger.info("Starting Zerodha Copy Trading System")
    
    # Create configuration manager
    config_manager = SecureConfigManager()
    
    # Check if configuration exists
    master_config = config_manager.load_master_config()
    follower_configs = config_manager.load_follower_configs()
    
    if not config_manager._validate_account_config(master_config):
        logger.error("Master account configuration is missing or invalid")
        print("\nERROR: Master account configuration is missing!")
        print("Please set the following environment variables:")
        print("- MASTER_API_KEY")
        print("- MASTER_API_SECRET") 
        print("- MASTER_ACCESS_TOKEN")
        print("- MASTER_USER_ID")
        print("\nOr create a .env file with these values.")
        return False
    
    if not follower_configs:
        logger.error("No follower account configurations found")
        print("\nERROR: No follower accounts configured!")
        print("Please set follower environment variables or create config.json")
        config_manager.create_sample_config_file()
        return False
    
    # Display configuration summary
    print(f"SUCCESS: Master account: {master_config.user_id}")
    print(f"SUCCESS: Follower accounts: {len(follower_configs)}")
    
    enabled_followers = [f for f in follower_configs if f.enabled]
    print(f"SUCCESS: Active followers: {len(enabled_followers)}")
    
    system_config = config_manager.get_system_config()
    print(f"SUCCESS: Paper trading mode: {system_config['paper_trading']}")
    print()
    
    # Safety confirmation
    if not system_config['paper_trading']:
        print("WARNING: Paper trading is DISABLED!")
        print("WARNING: This will place REAL TRADES with REAL MONEY!")
        print()
        response = input("Are you sure you want to continue? (type 'YES' to confirm): ")
        if response != 'YES':
            print("Operation cancelled for safety.")
            return False
    
    # Create and run the system
    try:
        copy_system = CopyTradingSystem(config_manager)
        success = copy_system.run()
        return success
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nSystem interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
