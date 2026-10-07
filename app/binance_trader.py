import os
from typing import Optional

from dotenv import load_dotenv
import ccxt

load_dotenv()


class BinanceTrader:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, testnet: bool = True):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.testnet = testnet

        if not self.api_key or not self.api_secret:
            raise ValueError("Missing BINANCE_API_KEY or BINANCE_API_SECRET in environment")

        self.exchange = ccxt.binance({
            "apiKey": self.api_key,
            "secret": self.api_secret,
            "enableRateLimit": True,
            "sandbox": testnet,
        })

    def get_balance(self):
        try:
            return self.exchange.fetch_balance()
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return None

    def get_ticker(self, symbol: str):
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            print(f"Error fetching ticker for {symbol}: {e}")
            return None

    def get_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 200):
        try:
            return self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        except Exception as e:
            print(f"Error fetching OHLCV for {symbol}: {e}")
            return []

    def create_order(self, symbol: str, side: str, amount: float, price: Optional[float] = None):
        try:
            if price is not None:
                return self.exchange.create_limit_order(symbol, side, amount, price)
            return self.exchange.create_market_order(symbol, side, amount)
        except Exception as e:
            print(f"Error creating order: {e}")
            return None

    def get_open_orders(self, symbol: Optional[str] = None):
        try:
            return self.exchange.fetch_open_orders(symbol)
        except Exception as e:
            print(f"Error fetching open orders: {e}")
            return []

    def cancel_order(self, symbol: str, order_id: str):
        try:
            return self.exchange.cancel_order(order_id, symbol)
        except Exception as e:
            print(f"Error cancelling order {order_id}: {e}")
            return None

    def get_position(self, symbol: str):
        try:
            positions = self.exchange.fetch_positions([symbol])
            for p in positions:
                if p.get("symbol") == symbol:
                    return p
            return None
        except Exception as e:
            print(f"Error fetching position for {symbol}: {e}")
            return None
