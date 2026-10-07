#!/usr/bin/env python
import sys
import pandas as pd
from app.backtest import run_backtest
from app.data import load_csv_data
from app.visualize import plot_backtest_results


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_backtest.py <csv_path>")
        print("Example: python run_backtest.py data/BTC_USDT_1h.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    
    try:
        print(f"Loading data from {csv_path}...")
        df = load_csv_data(csv_path)
        print(f"Loaded {len(df)} candles")
        
        print("Running backtest...")
        metrics, trader = run_backtest(df)
        
        print("\n" + "="*60)
        print("BACKTEST RESULTS")
        print("="*60)
        print(f"Total Trades:        {metrics['total_trades']}")
        print(f"Wins:                {metrics['wins']}")
        print(f"Losses:              {metrics['losses']}")
        print(f"Win Rate:            {metrics['win_rate']:.2%}")
        print(f"Total PnL:           ${metrics['total_pnl']:.2f}")
        print(f"Final Balance:       ${metrics['final_balance']:.2f}")
        print(f"Max Drawdown:        {metrics['max_drawdown']:.2%}")
        print(f"Profit Factor:       {metrics['profit_factor']:.2f}")
        print("="*60)
        
        if trader.closed_trades:
            print("\nRecent Trades:")
            for i, trade in enumerate(trader.closed_trades[-5:], 1):
                print(f"  {i}. {trade['side'].upper():5} @ {trade['entry_price']:.2f} -> {trade['exit_price']:.2f} | PnL: ${trade['pnl']:.2f} ({trade['reason']})")
        
        print("\nGenerating charts...")
        plot_backtest_results(df, trader)
        print("\nBacktest complete!")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during backtest: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
