import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample BTC/USDT data for testing
np.random.seed(42)
candles = 500
start_price = 45000

timestamps = [datetime(2024, 1, 1) + timedelta(hours=i) for i in range(candles)]
prices = [start_price]

for _ in range(candles - 1):
    change = np.random.normal(0, 200)
    prices.append(max(prices[-1] + change, 1))

data = {
    "timestamp": timestamps,
    "open": prices,
    "high": [p + np.random.uniform(0, 500) for p in prices],
    "low": [max(p - np.random.uniform(0, 500), 1) for p in prices],
    "close": [p + np.random.uniform(-300, 300) for p in prices],
    "volume": np.random.uniform(100, 1000, candles),
}

df = pd.DataFrame(data)
df.to_csv("data/BTC_USDT_1h_sample.csv", index=False)
print("Sample data created: data/BTC_USDT_1h_sample.csv")
