# master_client.py
import logging
import time
import json
from typing import Callable, Dict, Any, Optional
from kiteconnect import KiteConnect, KiteTicker
import threading
from dataclasses import asdict
from .config import AccountConfig

logger = logging.getLogger(__name__)

class MasterAccountClient:
    """
    Master account client that monitors trades using WebSocket connection.
    
    Features:
    - Real-time order updates via WebSocket
    - Automatic reconnection on connection loss
    - Trade filtering and validation
    - Event-driven architecture
    """
    
    def __init__(self, config: AccountConfig, on_trade_callback: Callable):
        self.config = config
        self.on_trade_callback = on_trade_callback
        
        # Initialize Kite Connect
        self.kite = KiteConnect(api_key=config.api_key)
        self.kite.set_access_token(config.access_token)
        
        # Initialize WebSocket ticker
        self.kws = KiteTicker(config.api_key, config.access_token)
        
        # Setup WebSocket callbacks
        self.kws.on_connect = self._on_connect
        self.kws.on_close = self._on_close
        self.kws.on_error = self._on_error
        self.kws.on_reconnect = self._on_reconnect
        self.kws.on_noreconnect = self._on_noreconnect
        self.kws.on_order_update = self._on_order_update
        
        # Connection state
        self.is_connected = False
        self.reconnect_count = 0
        self.max_reconnect_attempts = 10
        
        # Trade tracking
        self.processed_orders = set()
        
    def _on_connect(self, ws, response):
        """WebSocket connection established"""
        logger.info("WebSocket connected successfully")
        self.is_connected = True
        self.reconnect_count = 0
        
        # Subscribe to order updates
        try:
            self.kws.subscribe_order_update()
            logger.info("Subscribed to order updates")
        except Exception as e:
            logger.error(f"Error subscribing to order updates: {e}")
    
    def _on_close(self, ws, code, reason):
        """WebSocket connection closed"""
        logger.warning(f"WebSocket closed: {code} - {reason}")
        self.is_connected = False
    
    def _on_error(self, ws, code, reason):
        """WebSocket error occurred"""
        logger.error(f"WebSocket error: {code} - {reason}")
        self.is_connected = False
    
    def _on_reconnect(self, ws, reconnect_count):
        """WebSocket reconnection attempt"""
        logger.info(f"WebSocket reconnecting (attempt {reconnect_count})")
        self.reconnect_count = reconnect_count
    
    def _on_noreconnect(self, ws):
        """WebSocket failed to reconnect"""
        logger.error("WebSocket failed to reconnect")
        self.is_connected = False
        
        # Attempt manual reconnection after delay
        if self.reconnect_count < self.max_reconnect_attempts:
            threading.Timer(10.0, self._manual_reconnect).start()
    
    def _manual_reconnect(self):
        """Attempt manual reconnection"""
        try:
            logger.info("Attempting manual WebSocket reconnection")
            self.kws.connect(threaded=True)
        except Exception as e:
            logger.error(f"Manual reconnection failed: {e}")
            if self.reconnect_count < self.max_reconnect_attempts:
                threading.Timer(30.0, self._manual_reconnect).start()
    
    def _on_order_update(self, ws, data):
        """Handle order update events"""
        try:
            logger.info(f"Order update received: {data}")
            
            # Only process completed orders
            if data.get('status') == 'COMPLETE':
                order_id = data.get('order_id')
                
                # Avoid processing the same order multiple times
                if order_id in self.processed_orders:
                    return
                
                self.processed_orders.add(order_id)
                
                # Extract trade details
                trade_data = {
                    'order_id': order_id,
                    'tradingsymbol': data.get('tradingsymbol'),
                    'exchange': data.get('exchange'),
                    'transaction_type': data.get('transaction_type'),
                    'quantity': data.get('quantity', 0),
                    'price': data.get('price', 0),
                    'product': data.get('product'),
                    'order_type': data.get('order_type'),
                    'timestamp': data.get('order_timestamp'),
                    'user_id': self.config.user_id
                }
                
                # Validate trade data
                if self._validate_trade_data(trade_data):
                    logger.info(f"Valid trade detected: {trade_data}")
                    
                    # Call the callback function to notify followers
                    try:
                        self.on_trade_callback(trade_data)
                    except Exception as e:
                        logger.error(f"Error in trade callback: {e}")
                else:
                    logger.warning(f"Invalid trade data received: {trade_data}")
                    
        except Exception as e:
            logger.error(f"Error processing order update: {e}")
    
    def _validate_trade_data(self, trade_data: Dict[str, Any]) -> bool:
        """Validate trade data before processing with multi-segment support"""
        required_fields = ['tradingsymbol', 'exchange', 'transaction_type', 'quantity', 'product']
        
        # Check required fields
        for field in required_fields:
            if not trade_data.get(field):
                logger.warning(f"Missing required field: {field}")
                return False
        
        # Validate quantity
        if trade_data['quantity'] <= 0:
            logger.warning(f"Invalid quantity: {trade_data['quantity']}")
            return False
        
        # Validate transaction type
        if trade_data['transaction_type'] not in ['BUY', 'SELL']:
            logger.warning(f"Invalid transaction type: {trade_data['transaction_type']}")
            return False
        
        # Validate exchange
        valid_exchanges = ['NSE', 'BSE', 'NFO', 'MCX', 'BFO', 'CDS']
        exchange = trade_data.get('exchange')
        if exchange not in valid_exchanges:
            logger.warning(f"Unknown exchange: {exchange}")
            # Don't reject - might be a new exchange we haven't seen
        
        # Segment-specific validations
        symbol = trade_data.get('tradingsymbol', '')
        
        if exchange == 'MCX':
            # Commodity symbols validation
            logger.info(f"Commodity trade detected: {symbol}")
            # MCX symbols are typically like GOLD21DECFUT, CRUDEOIL21NOVFUT etc.
            
        elif exchange == 'NFO':
            # NSE F&O validation
            if 'FUT' in symbol or 'CE' in symbol or 'PE' in symbol:
                logger.info(f"NSE F&O trade detected: {symbol}")
            
        elif exchange == 'BFO':
            # BSE F&O validation
            logger.info(f"BSE F&O trade detected: {symbol}")
            
        elif exchange == 'CDS':
            # Currency validation
            logger.info(f"Currency derivative trade detected: {symbol}")
            
        elif exchange in ['NSE', 'BSE']:
            # Equity validation
            logger.info(f"Equity trade detected on {exchange}: {symbol}")
        
        return True
    
    def start_monitoring(self):
        """Start monitoring master account trades"""
        try:
            logger.info("Starting master account monitoring...")
            
            # Test API connection first
            profile = self.kite.profile()
            logger.info(f"Connected to master account: {profile['user_name']} ({profile['user_id']})")
            
            # Start WebSocket connection
            self.kws.connect(threaded=True)
            
            logger.info("Master account monitoring started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start master account monitoring: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop monitoring master account trades"""
        try:
            logger.info("Stopping master account monitoring...")
            
            if self.kws:
                self.kws.close()
            
            self.is_connected = False
            logger.info("Master account monitoring stopped")
            
        except Exception as e:
            logger.error(f"Error stopping master account monitoring: {e}")
    
    def get_connection_status(self) -> Dict[str, Any]:
        """Get current connection status"""
        return {
            'connected': self.is_connected,
            'reconnect_count': self.reconnect_count,
            'processed_orders': len(self.processed_orders)
        }
