# Invest Alchemy

Invest Alchemy is a trade assistant for A share stock market.

## TODO

- Feature
  - Strategy
    - [x] Double MA
    - [ ] Turtle
    - [ ] Backtrace MA250
    - [ ] Breakthrough Platform
    - [ ] Keep Increasing
    - [ ] Low Atr
  - Market
    - [ ] Index Historical P/E Ratio
    - [x] Base database store baseline (10%) and popular indexs performance (000905/000300/399006/HSI/IXIC/INX)
  - Portfolio
    - [x] Transaction/Funding/Holding/NetValue/Performance Ledger
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
    - [ ] Re-Design web UI page 🚩
  - Notify
    - [x] Email
    - [x] Telegram bot/channel
    - [ ] Show different strategy signal (daily)
    - [ ] Show different trade robot portfolio performance report (weekly)

- Arch Improve
  - Storage
    - [x] Add database schema migration tool
    - [x] SQLite DB backup to AWS S3
    - [x] Trade data store in SQLite DB
    - [x] Base Database migrate from SQLite to Supabase(PostgreSQL) 

- Bug Fix
  - [x] Trading signals error when double ma price are same

## Note

### Strategy

- Trade strategy
  - [Sequoia](https://github.com/sngyai/Sequoia)

- Issue
  - **Split-adjusted share prices**: Use `qfq` adjust price to generate trade signals.

### Portfolio

- **Split-adjusted share prices**: Not processed in the trading ledger (only robots, **user trader need add a transaction when split-adjusted happens**), but processed in the holding ledger calculation.
  - [x] 🐛 Robot user still can not process, because split-adjusted check on the portfolio net value ledger calculation, but sell transaction amount do not equal to holding amount because sell transaction generated on the transaction ledger calculation, so it needs to process on portfolio net value calculation when user is a robot type.
    - Fix this issue by: robot trader use `qfq` adjust price while user trader use close price when calculate the portfolio net value (include transaction/holdings/net value ledger calculation), user trader need add a transaction when split-adjusted happens to adjust the hold amount.

### Robot Trader

- **About the slippage issue**: Since the underlying traded are daily level ETFs, the impact of slippage issues is minimal.
- **No liquidity issues**: Because simulation trading cannot know the liquidity of the transaction of the day, such as A shares max up and down the restrictions caused the inability to deal, there is a certain deviation from the actual transaction, which is also the charm of the real deal, there is a certain amount of uncertainty brought about by the change.
- **About dividends**: The robot trader will ignore the case of dividends on the holding position, because the calculation will be complicated. However, real user trader can manually record dividends as one transaction.

## Post

- [Serverless应用开发小记](https://www.bmpi.dev/dev/guide-to-serverless/)
- [Adventures in Serverless Application Development](https://www.bmpi.dev/en/dev/guide-to-serverless/)

## Video Log

- [Invest Alchemy Dev Log](https://youtu.be/i3RDqAd9LKs)
