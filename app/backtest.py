import pandas as pd

from app.paper_trader import PaperTrader
from app.strategy import generate_signals


def calculate_metrics(trader: PaperTrader) -> dict:
    trades = trader.closed_trades
    if not trades:
        return {
            "total_trades": 0,
            "win_rate": 0.0,
            "total_pnl": 0.0,
            "final_balance": trader.balance,
            "max_drawdown": trader.max_drawdown,
            "profit_factor": 0.0,
        }

    wins = sum(1 for trade in trades if trade["pnl"] > 0)
    total = len(trades)
    total_profit = sum(trade["pnl"] for trade in trades if trade["pnl"] > 0)
    total_loss = abs(sum(trade["pnl"] for trade in trades if trade["pnl"] < 0))

    return {
        "total_trades": total,
        "wins": wins,
        "losses": total - wins,
        "win_rate": wins / total if total else 0.0,
        "total_pnl": trader.total_pnl,
        "final_balance": trader.balance,
        "max_drawdown": trader.max_drawdown,
        "profit_factor": total_profit / total_loss if total_loss else float("inf"),
    }


def run_backtest(df: pd.DataFrame) -> tuple[dict, PaperTrader]:
    signal_df = generate_signals(df)
    trader = PaperTrader()

    for row in signal_df.itertuples(index=False):
        signal = int(getattr(row, "signal"))
        timestamp = getattr(row, "timestamp")
        close = float(getattr(row, "close"))
        low = float(getattr(row, "low"))
        high = float(getattr(row, "high"))

        if trader.position_side is None and signal != 0:
            trader.open_position(close, signal, timestamp)

        if trader.position_side is not None:
            if trader.check_daily_loss_limit():
                trader.close_position(close, "daily_loss_limit", timestamp)
                continue

            if trader.check_drawdown_limit():
                trader.close_position(close, "drawdown_limit", timestamp)
                continue

            if trader.check_stop_loss(low, high, timestamp):
                continue

            if trader.check_take_profit(low, high, timestamp):
                continue

            if trader.position_side == "long" and signal == -1:
                trader.close_position(close, "signal_exit", timestamp)
            elif trader.position_side == "short" and signal == 1:
                trader.close_position(close, "signal_exit", timestamp)

        trader.update_equity(timestamp)

    metrics = calculate_metrics(trader)
    return metrics, trader
