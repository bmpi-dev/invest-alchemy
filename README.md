# Invest Alchemy

Invest Alchemy is a trade assistant for A share stock market.

## TODO

- Feature
  - Strategy
    - [x] ETF Double MA
  - Market
    - [ ] Index Historical P/E Ratio
    - [ ] Base database store baseline (10%) and popular indexs performance (000905/000300/399006/HSI/IXIC/INX)
  - Portfolio
    - [ ] Transaction/Funding/Holding/NetValue/Performance Ledger 🚩
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
    - [ ] Base Database migrate from SQLite to Supabase(PostgreSQL)

- Bug Fix
  - [x] Trading signals error when double ma price are same

## Note

### Portfolio

- **Split-adjusted share prices**: Not processed in the trading ledger (including users and robots), but processed in the holding ledger calculation.

## Post

- [Serverless应用开发小记](https://www.bmpi.dev/dev/guide-to-serverless/)
- [Adventures in Serverless Application Development](https://www.bmpi.dev/en/dev/guide-to-serverless/)
