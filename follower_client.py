# follower_client.py
import logging
import time
from typing import Dict, Any, Optional
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException
from config import AccountConfig

logger = logging.getLogger(__name__)

class FollowerAccountClient:
    """
    Follower account client that replicates trades from master account.
    
    Features:
    - Automatic trade replication with quantity scaling
    - Risk management and position limits
    - Comprehensive error handling and retry logic
    - Trade execution logging and monitoring
    """
    
    def __init__(self, config: AccountConfig):
        self.config = config
        
        # Initialize Kite Connect
        self.kite = KiteConnect(api_key=config.api_key)
        self.kite.set_access_token(config.access_token)
        
        # Risk management
        self.daily_trades_count = 0
        self.daily_pnl = 0.0
        self.max_daily_trades = 100
        self.max_daily_loss = 10000.0
        
        # Order tracking
        self.placed_orders = []
        self.failed_orders = []
        
        # Rate limiting
        self.last_order_time = 0
        self.min_order_interval = 1.0  # seconds
        
    def validate_connection(self) -> bool:
        """Validate API connection and credentials"""
        try:
            profile = self.kite.profile()
            logger.info(f"Follower account validated: {profile['user_name']} ({profile['user_id']})")
            return True
        except Exception as e:
            logger.error(f"Follower account validation failed: {e}")
            return False
    
    def _check_risk_limits(self, trade_data: Dict[str, Any]) -> tuple[bool, str]:
        """Check if trade is within risk limits"""
        
        # Check if account is enabled
        if not self.config.enabled:
            return False, "Account is disabled"
        
        # Check daily trade limit
        if self.daily_trades_count >= self.max_daily_trades:
            return False, f"Daily trade limit reached ({self.max_daily_trades})"
        
        # Check position size limit
        adjusted_quantity = int(trade_data['quantity'] * self.config.multiplier)
        if adjusted_quantity > self.config.max_position_size:
            return False, f"Position size limit exceeded ({adjusted_quantity} > {self.config.max_position_size})"
        
        # Check daily loss limit
        if self.daily_pnl < -self.max_daily_loss:
            return False, f"Daily loss limit reached ({self.daily_pnl})"
        
        # Rate limiting check
        current_time = time.time()
        if current_time - self.last_order_time < self.min_order_interval:
            time_to_wait = self.min_order_interval - (current_time - self.last_order_time)
            time.sleep(time_to_wait)
        
        return True, "Risk check passed"
    
    def _calculate_quantity(self, original_quantity: int) -> int:
        """Calculate adjusted quantity based on multiplier"""
        adjusted_quantity = int(original_quantity * self.config.multiplier)
        
        # Ensure minimum quantity of 1
        if adjusted_quantity < 1 and self.config.multiplier > 0:
            adjusted_quantity = 1
        
        return adjusted_quantity
    
    def _place_order_with_retry(self, order_params: Dict[str, Any], max_retries: int = 3) -> Optional[str]:
        """Place order with retry logic"""
        
        for attempt in range(max_retries):
            try:
                # Place the order
                order_id = self.kite.place_order(**order_params)
                
                logger.info(f"Order placed successfully: {order_id} - {order_params}")
                
                # Update tracking
                self.last_order_time = time.time()
                self.daily_trades_count += 1
                self.placed_orders.append({
                    'order_id': order_id,
                    'params': order_params,
                    'timestamp': time.time()
                })
                
                return order_id
                
            except KiteException as e:
                error_msg = f"Kite API error (attempt {attempt + 1}/{max_retries}): {e}"
                logger.error(error_msg)
                
                # Check if error is retryable
                if e.code in [429, 500, 502, 503, 504]:  # Rate limit or server errors
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 1  # Exponential backoff
                        logger.info(f"Retrying after {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                
                # Log non-retryable errors
                self.failed_orders.append({
                    'params': order_params,
                    'error': str(e),
                    'timestamp': time.time()
                })
                break
                
            except Exception as e:
                error_msg = f"Unexpected error (attempt {attempt + 1}/{max_retries}): {e}"
                logger.error(error_msg)
                
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                
                self.failed_orders.append({
                    'params': order_params,
                    'error': str(e),
                    'timestamp': time.time()
                })
                break
        
        return None
    
    def replicate_trade(self, master_trade: Dict[str, Any]) -> bool:
        """Replicate a trade from the master account"""
        
        try:
            logger.info(f"Replicating trade for follower {self.config.user_id}: {master_trade}")
            
            # Check risk limits
            risk_check_passed, risk_message = self._check_risk_limits(master_trade)
            if not risk_check_passed:
                logger.warning(f"Trade blocked by risk management: {risk_message}")
                return False
            
            # Calculate adjusted quantity
            adjusted_quantity = self._calculate_quantity(master_trade['quantity'])
            
            if adjusted_quantity <= 0:
                logger.warning("Adjusted quantity is zero or negative, skipping trade")
                return False
            
            # Prepare order parameters
            order_params = {
                'variety': 'regular',
                'exchange': master_trade['exchange'],
                'tradingsymbol': master_trade['tradingsymbol'],
                'transaction_type': master_trade['transaction_type'],
                'quantity': adjusted_quantity,
                'product': master_trade['product'],
                'order_type': 'MARKET',  # Use market orders for immediate execution
                'tag': f"copy_trade_{master_trade.get('order_id', 'unknown')}"
            }
            
            # Handle limit orders (optional feature)
            if master_trade.get('order_type') == 'LIMIT' and master_trade.get('price'):
                order_params['order_type'] = 'LIMIT'
                order_params['price'] = master_trade['price']
            
            logger.info(f"Placing follower order: {order_params}")
            
            # Place the order
            order_id = self._place_order_with_retry(order_params)
            
            if order_id:
                logger.info(f"Trade replicated successfully: Order ID {order_id}")
                return True
            else:
                logger.error("Failed to replicate trade after all retry attempts")
                return False
                
        except Exception as e:
            logger.error(f"Error replicating trade: {e}")
            return False
    
    def get_account_status(self) -> Dict[str, Any]:
        """Get current account status and statistics"""
        return {
            'user_id': self.config.user_id,
            'enabled': self.config.enabled,
            'multiplier': self.config.multiplier,
            'daily_trades_count': self.daily_trades_count,
            'daily_pnl': self.daily_pnl,
            'placed_orders': len(self.placed_orders),
            'failed_orders': len(self.failed_orders),
            'max_position_size': self.config.max_position_size
        }
    
    def reset_daily_stats(self):
        """Reset daily statistics (call at market open)"""
        self.daily_trades_count = 0
        self.daily_pnl = 0.0
        self.placed_orders = []
        self.failed_orders = []
        logger.info(f"Daily statistics reset for follower {self.config.user_id}")
