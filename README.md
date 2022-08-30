# Invest Alchemy

Invest Alchemy is a trade assistant for A share stock market.

## TODO

- Feature
  - Strategy
    - [x] ETF Double MA
  - Market
    - [ ] Index Historical P/E Ratio
    - [ ] Base database store baseline (10%) and popular indexs performance (000905/000300/399006/HSI/IXIC/INX) 🚩
  - Portfolio
    - [x] Transaction/Funding/Holding/NetValue/Performance Ledger
  - Trader
    - User
      - [ ] User portfolio calculation support
    - Robot
      - Double MA (11/22)
        - [x] Long ETF strategy robot trader
        - [x] All In strategy robot trader
        - [ ] Periodic Payment strategy robot trader
  - Web UI
    - [ ] Re-Design web UI page
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

### Portfolio

- **Split-adjusted share prices**: Not processed in the trading ledger (including users and robots), but processed in the holding ledger calculation.

### Robot Trader

- **About the slippage issue**: Since the underlying traded are daily level ETFs, the impact of slippage issues is minimal.
- **No liquidity issues**: Because simulation trading cannot know the liquidity of the transaction of the day, such as A shares max up and down the restrictions caused the inability to deal, there is a certain deviation from the actual transaction, which is also the charm of the real deal, there is a certain amount of uncertainty brought about by the change.

## Post

- [Serverless应用开发小记](https://www.bmpi.dev/dev/guide-to-serverless/)
- [Adventures in Serverless Application Development](https://www.bmpi.dev/en/dev/guide-to-serverless/)

## Video Log

- [Invest Alchemy Dev Log](https://youtu.be/i3RDqAd9LKs)
