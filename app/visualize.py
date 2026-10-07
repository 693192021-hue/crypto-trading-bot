import pandas as pd
import matplotlib.pyplot as plt
from app.backtest import run_backtest


def plot_backtest_results(df: pd.DataFrame, trader) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Equity curve
    equity_df = pd.DataFrame(trader.equity_curve)
    axes[0, 0].plot(equity_df["timestamp"], equity_df["equity"], label="Equity", linewidth=2)
    axes[0, 0].set_title("Equity Curve")
    axes[0, 0].set_xlabel("Timestamp")
    axes[0, 0].set_ylabel("Balance ($)")
    axes[0, 0].legend()
    axes[0, 0].grid(True)

    # Profit/Loss per trade
    if trader.closed_trades:
        pnls = [t["pnl"] for t in trader.closed_trades]
        axes[0, 1].bar(range(len(pnls)), pnls, color=["green" if p > 0 else "red" for p in pnls])
        axes[0, 1].set_title("PnL per Trade")
        axes[0, 1].set_xlabel("Trade Number")
        axes[0, 1].set_ylabel("PnL ($)")
        axes[0, 1].grid(True)
    
    # Cumulative PnL
    if trader.closed_trades:
        cumulative_pnl = []
        total = 0
        for t in trader.closed_trades:
            total += t["pnl"]
            cumulative_pnl.append(total)
        axes[1, 0].plot(range(len(cumulative_pnl)), cumulative_pnl, label="Cumulative PnL", linewidth=2)
        axes[1, 0].set_title("Cumulative PnL")
        axes[1, 0].set_xlabel("Trade Number")
        axes[1, 0].set_ylabel("PnL ($)")
        axes[1, 0].legend()
        axes[1, 0].grid(True)
    
    # Drawdown
    if trader.equity_curve:
        equity_vals = [e["equity"] for e in trader.equity_curve]
        peak = equity_vals[0]
        drawdowns = []
        for e in equity_vals:
            if e > peak:
                peak = e
            dd = (peak - e) / peak * 100 if peak > 0 else 0
            drawdowns.append(dd)
        axes[1, 1].fill_between(range(len(drawdowns)), drawdowns, alpha=0.3, color="red")
        axes[1, 1].plot(range(len(drawdowns)), drawdowns, color="red", linewidth=1.5, label="Drawdown")
        axes[1, 1].set_title("Drawdown")
        axes[1, 1].set_xlabel("Candle")
        axes[1, 1].set_ylabel("Drawdown (%)")
        axes[1, 1].legend()
        axes[1, 1].grid(True)
    
    plt.tight_layout()
    plt.savefig("backtest_results.png", dpi=100)
    print("Chart saved to backtest_results.png")
    plt.close()
