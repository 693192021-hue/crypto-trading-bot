# Crypto Trading Bot - Paper Trading Backtest

一个基于 Python 的加密货币交易机器人框架，专注于**纸交易、回测和风控**。

## 特性

- ✅ EMA + RSI 策略
- ✅ 纸交易模拟（不直接交易）
- ✅ 完整的风险控制
  - 单笔风险限制 1%
  - 止损 2%
  - 止盈 4%
  - 最大日亏损限制 2%
  - 最大回撤限制 10%
- ✅ 历史数据回测
- ✅ 交易统计和可视化
- ✅ Binance 数据下载

## 快速开始

### 1. 安装

```bash
git clone https://github.com/693192021-hue/crypto-trading-bot.git
cd crypto-trading-bot

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 获取数据

#### 方式 A: 使用 Binance API 下载最新数据

```bash
python -m app.download_data BTC/USDT 1h 1000
```

这会下载最近 1000 个 1h K 线，保存到 `data/BTC_USDT_1h.csv`

#### 方式 B: 使用示例数据

```bash
python data/sample_data.py
```

### 3. 运行回测

```bash
python run_backtest.py data/BTC_USDT_1h_sample.csv
```

输出示例：

```
============================================================
BACKTEST RESULTS
============================================================
Total Trades:        42
Wins:                28
Losses:              14
Win Rate:            66.67%
Total PnL:           $1250.50
Final Balance:       $11250.50
Max Drawdown:        5.23%
Profit Factor:       3.45
============================================================
```

## 配置

编辑 `.env` 文件来自定义交易参数：

```bash
cp .env.example .env
```

```env
ACCOUNT_BALANCE=10000          # 初始账户余额
RISK_PER_TRADE=0.01           # 单笔风险比例 (1%)
MAX_DAILY_LOSS=0.02           # 最大日亏损 (2%)
MAX_DRAWDOWN=0.10             # 最大回撤 (10%)
STOP_LOSS_PCT=0.02            # 止损 (2%)
TAKE_PROFIT_PCT=0.04          # 止盈 (4%)
```

## 策略说明

### EMA + RSI 策略

**买入条件：**
- EMA 9 > EMA 21（短期趋势向上）
- RSI > 50（动量确认）

**卖出条件：**
- EMA 9 < EMA 21（短期趋势向下）
- RSI < 50（动量确认）

### 风险管理

1. **单笔风险**：每笔交易最多亏损账户的 1%
2. **止损**：每笔交易止损设置在入场价格下方 2%
3. **止盈**：每笔交易止盈设置在入场价格上方 4%
4. **日亏损限制**：单日累计亏损达到 2% 时停止交易
5. **最大回撤**：账户回撤超过 10% 时停止交易

## 项目结构

```
crypto-trading-bot/
├── app/
│   ├── config.py           # 配置文件
│   ├── strategy.py         # EMA + RSI 策略
│   ├── risk_manager.py     # 风险管理
│   ├── paper_trader.py     # 纸交易账户
│   ├── backtest.py         # 回测引擎
│   ├── data.py             # 数据加载
│   ├── download_data.py    # 数据下载
│   └── visualize.py        # 结果可视化
├── data/
│   ├── sample_data.py      # 生成示例数据
│   └── *.csv               # K 线数据
├── run_backtest.py         # 主入口
├── requirements.txt        # 依赖
├── .env.example            # 环境变量模板
└── README.md
```

## CSV 数据格式

CSV 文件必须包含以下列：

| 列名 | 说明 | 示例 |
|------|------|------|
| timestamp | 时间戳 | 2024-01-01 00:00:00 |
| open | 开盘价 | 45000.50 |
| high | 最高价 | 45500.00 |
| low | 最低价 | 44500.00 |
| close | 收盘价 | 45100.00 |
| volume | 成交量 | 1234.56 |

## 使用 Binance 数据

需要先安装 ccxt：

```bash
pip install ccxt
```

然后下载数据：

```bash
python -m app.download_data BTC/USDT 1h 1000
python -m app.download_data ETH/USDT 4h 500
```

## 重要提示

⚠️ **这是一个学习和回测项目，不建议直接用于真实账户实盘交易。**

- 先做充分的历史回测
- 再用纸交易验证策略
- 最后再考虑实盘交易
- 始终设置止损和仓位控制

## 下一步计划

- [ ] 多策略支持
- [ ] 多币种组合
- [ ] 参数优化框架
- [ ] 实时纸交易（WebSocket）
- [ ] 实盘交易接口
- [ ] 策略性能对比
- [ ] 风险收益曲线优化

## 联系方式

如有问题或建议，欢迎提交 Issue 或 PR。

## License

MIT
