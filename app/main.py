from __future__ import annotations

import argparse

from app.backtest import run_backtest
from app.data import load_csv_data


def main() -> None:
    parser = argparse.ArgumentParser(description="Crypto paper trading backtest")
    parser.add_argument("--csv", required=True, help="Path to OHLCV CSV file")
    args = parser.parse_args()

    df = load_csv_data(args.csv)
    metrics, trader = run_backtest(df)

    print("Backtest result:")
    print(f"Total trades: {metrics['total_trades']}")
    print(f"Win rate: {metrics['win_rate']:.2%}")
    print(f"Total PnL: {metrics['total_pnl']:.2f}")
    print(f"Final balance: {metrics['final_balance']:.2f}")
    print(f"Max drawdown: {metrics['max_drawdown']:.2%}")
    print(f"Profit factor: {metrics['profit_factor']:.2f}")

    if trader.closed_trades:
        print("Latest trades:")
        for trade in trader.closed_trades[-5:]:
            print(trade)


if __name__ == "__main__":
    main()
