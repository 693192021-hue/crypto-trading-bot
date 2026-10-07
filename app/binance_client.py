import ccxt
import os
from dotenv import load_dotenv

load_dotenv()


class BinanceClient:
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        """
        Initialize Binance client
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet (True) or mainnet (False)
        """
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.testnet = testnet
        
        if not self.api_key or not self.api_secret:
            raise ValueError("BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env or passed as arguments")
        
        # Initialize exchange
        self.exchange = ccxt.binance({
            "apiKey": self.api_key,
            "secret": self.api_secret,
            "enableRateLimit": True,
            "sandbox": testnet,  # Use testnet
        })
        
        print(f"Connected to Binance {'Testnet' if testnet else 'Mainnet'}")

    def get_balance(self):
        """Get account balance"""
        try:
            balance = self.exchange.fetch_balance()
            return balance
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None

    def get_ticker(self, symbol):
        """Get ticker info"""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        except Exception as e:
            print(f"Error fetching ticker: {e}")
            return None

    def place_limit_order(self, symbol, side, amount, price):
        """
        Place a limit order
        
        Args:
            symbol: Trading pair (e.g., BTC/USDT)
            side: 'buy' or 'sell'
            amount: Order quantity
            price: Order price
        """
        try:
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            print(f"Order placed: {order}")
            return order
        except Exception as e:
            print(f"Error placing order: {e}")
            return None

    def place_market_order(self, symbol, side, amount):
        """
        Place a market order
        
        Args:
            symbol: Trading pair (e.g., BTC/USDT)
            side: 'buy' or 'sell'
            amount: Order quantity
        """
        try:
            order = self.exchange.create_market_order(symbol, side, amount)
            print(f"Market order placed: {order}")
            return order
        except Exception as e:
            print(f"Error placing market order: {e}")
            return None

    def cancel_order(self, symbol, order_id):
        """Cancel an order"""
        try:
            result = self.exchange.cancel_order(order_id, symbol)
            print(f"Order cancelled: {result}")
            return result
        except Exception as e:
            print(f"Error cancelling order: {e}")
            return None

    def get_open_orders(self, symbol=None):
        """Get open orders"""
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            return orders
        except Exception as e:
            print(f"Error fetching open orders: {e}")
            return None

    def get_closed_orders(self, symbol=None, limit=10):
        """Get closed orders"""
        try:
            orders = self.exchange.fetch_closed_orders(symbol, limit=limit)
            return orders
        except Exception as e:
            print(f"Error fetching closed orders: {e}")
            return None

    def get_order_status(self, symbol, order_id):
        """Get order status"""
        try:
            order = self.exchange.fetch_order(order_id, symbol)
            return order
        except Exception as e:
            print(f"Error fetching order status: {e}")
            return None

    def get_real_time_price(self, symbol):
        """Get real-time price"""
        try:
            ticker = self.fetch_ticker(symbol)
            return ticker['last']
        except Exception as e:
            print(f"Error fetching real-time price: {e}")
            return None
