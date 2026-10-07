import ccxt
import pandas as pd
from datetime import datetime


def download_binance_data(symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 1000) -> pd.DataFrame:
    exchange = ccxt.binance({
        "enableRateLimit": True,
    })
    
    print(f"Downloading {symbol} {timeframe} data from Binance...")
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    
    df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    
    filename = f"data/{symbol.replace('/', '_')}_{timeframe}.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    
    return df


if __name__ == "__main__":
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTC/USDT"
    timeframe = sys.argv[2] if len(sys.argv) > 2 else "1h"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
    
    download_binance_data(symbol, timeframe, limit)
