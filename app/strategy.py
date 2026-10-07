import numpy as np
import pandas as pd


def calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=window - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=window - 1, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def generate_signals(df: pd.DataFrame, fast_window: int = 9, slow_window: int = 21, rsi_window: int = 14) -> pd.DataFrame:
    result = df.copy()
    result["ema_fast"] = result["close"].ewm(span=fast_window, adjust=False).mean()
    result["ema_slow"] = result["close"].ewm(span=slow_window, adjust=False).mean()
    result["rsi"] = calculate_rsi(result["close"], window=rsi_window)

    result["signal"] = 0
    result.loc[(result["ema_fast"] > result["ema_slow"]) & (result["rsi"] > 50), "signal"] = 1
    result.loc[(result["ema_fast"] < result["ema_slow"]) & (result["rsi"] < 50), "signal"] = -1

    return result

