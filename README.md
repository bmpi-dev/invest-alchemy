# Invest Alchemy

Invest Alchemy is a trading assistant focused on ETF portfolios. For more context, see this [post](https://www.bmpi.dev/money/invest-alchemy/).

## TODO

- Feature
  - Data
    - [x] [Tushare](https://tushare.pro/)
    - [ ] [AKShare](https://akshare.xyz/)
    - Other
      - [理杏仁](https://www.lixinger.com/)
      - [Yahoo](https://finance.yahoo.com/)
      - [ETF.com](https://www.etf.com/)
      - [ETFDB.com](https://etfdb.com/)
  - Strategy
    - Trade strategies
      - [x] Double MA
      - [ ] Turtle
      - [ ] Backtrace MA250
      - [ ] Breakthrough Platform
      - [ ] Keep Increasing
      - [ ] Low Atr
    - Trade backtesting
      - [ ] Spike [backtrader](https://github.com/mementum/backtrader), maybe we can use it to do the strategy backtesting before we go to implement the strategy signal.
    - [ ] ETF similarity calculation, can filter similar ETF
      - https://www.etf.com/etfanalytics/etf-comparison-tool
  - Market
    - [ ] Support USA share ETF
    - [ ] Index Historical P/E Ratio
    - [x] Base database store baseline (10%) and popular indexs performance (000905/000300/399006/HSI/IXIC/INX)
  - Portfolio
    - [x] Transaction/Funding/Holding/NetValue/Performance Ledger
      - [ ] Add portfolio fund utilization performance (holding assets / total assets)
    - [x] Add popular indexs net value compare Ledger
    - [x] Support trade A share ETF/LOF funds
    - [x] Support trade A share stock
    - [ ] Support trade A public funds (not include ETF/LOF)
  - Trader
    - User
      - [x] User portfolio calculation support
    - Robot
      - Double MA (11/22)
        - [x] Long ETF strategy robot trader
        - [x] All In strategy robot trader
        - [ ] Periodic Payment strategy robot trader
  - Web UI
    - [x] Re-Design web UI page
      - [x] Portfolio Risk Monitor
      - [x] Portfolio holding/transaction/funding history
  - Notify
    - [x] Email
    - [x] Telegram bot/channel
    - [ ] Slack bot/channel
    - [ ] Show different strategy signal (daily)
    - [ ] Show different trade robot portfolio performance report (weekly)
    - [ ] Can subscribe trade event of the special portfolio by email/rss

- Arch Improve
  - Storage
    - [x] Add database schema migration tool
    - [x] SQLite DB backup to AWS S3
    - [x] Trade data store in SQLite DB
    - [x] Base Database migrate from SQLite to Supabase(PostgreSQL) 

- Bug Fix
  - [x] Trading signals error when double ma price are same.
  - [ ] Portfolio performance ledger max_days_of_continuous_loss calculation error, max is 5, because the days_of_continuous_loss will set to 0 when on non-trade days.

## Note

### Strategy

- Trade strategy
  - [Sequoia](https://github.com/sngyai/Sequoia)

- Issue
  - **Split-adjusted share prices**: Use `qfq` adjust price to generate trade signals.
  
- Note
  - Why the trade strategy may not good at trading stock?
    - Compare index, stocks have the liquidity problem and suspension risk. Liquidity can lead to a huge gap between simulated trading and actual trading results, suspension will result in inability to trade, producing results that are completely different from simulated trading.
  - **About strategy backtesting overfitting**: Backtesting overfitting may be a killer in trade stragety, so we not pursue the profit maximization by overfitting, just using the simple trade strategy to overcome the market volatility.

### Portfolio

- **Split-adjusted share prices**: Not processed in the trading ledger (only robots, **user trader need add a transaction when split-adjusted happens**), but processed in the holding ledger calculation.
  - [x] 🐛 Robot user still can not process, because split-adjusted check on the portfolio net value ledger calculation, but sell transaction amount do not equal to holding amount because sell transaction generated on the transaction ledger calculation, so it needs to process on portfolio net value calculation when user is a robot type.
    - ~~Fix this issue by: robot trader use `qfq` adjust price while user trader use close price when calculate the portfolio net value (include transaction/holdings/net value ledger calculation), user trader need add a transaction when split-adjusted happens to adjust the hold amount.~~
      - `qfq` cannot fix this issue, because if the split-adjusted share happens, `qfq` only change it's hsitory price, e.g. the day before split-adjusted day(20220904), 512100.SH close price is 0.982, today(20220905) the close price is 2.713, if the hold amount is not changed, the market value of it will change to nearly three times than before.
    - Fix by changing the hold amout when split-adjusted happens and this must happens on the generated transaction csv file phase (if not, the robot trader can not know what amount it can sell). Although this solution can slow the calculation speed, but currently it is the most easy way to fix it.

### Robot Trader

- **About the slippage issue**: Since the underlying traded are daily level ETFs, the impact of slippage issues is minimal.
- **About the no liquidity issues**: Because simulation trading cannot know the liquidity of the transaction of the day, such as A shares max up and down the restrictions caused the inability to deal, there is a certain deviation from the actual transaction, which is also the charm of the real deal, there is a certain amount of uncertainty brought about by the change.
- **About dividends**: The robot trader will ignore the case of dividends on the holding position, because the calculation will be complicated. However, real user trader can manually record dividends as one transaction.
- **About trade fees**: Because the ETF/LOF trade fees in A share market is very low, so robot trader just ignore the trade fees for simplified calculations.

## Post

- [投资炼金术](https://www.bmpi.dev/money/invest-alchemy/)
- [Serverless应用开发小记](https://www.bmpi.dev/dev/guide-to-serverless/)
- [Adventures in Serverless Application Development](https://www.bmpi.dev/en/dev/guide-to-serverless/)

## Video Log

- [Invest Alchemy Dev Log](https://youtu.be/i3RDqAd9LKs)
