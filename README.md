# Invest Alchemy

Invest Alchemy is a trade assistant for A share stock market.

## TODO

- Feature
  - Stategy
    - [x] ETF Double MA
  - Market Heat Meter
    - [ ] Index Historical P/E Ratio
  - Trading Portfolio Calculation
    - [ ] Transaction/Funding/Holding/NetValue/Performance Ledger
  - Trader
    - User
      - [ ] User portfolio calculation support
    - Robot
      - Double MA (11/22)
        - [x] Long ETF strategy robot trader
        - [x] All In strategy robot trader
        - [ ] Periodic Payment strategy robot trader
   - Web
    - [ ] Re-Design web UI page
- Improve
  - Notify
    - [x] Email
    - [x] Telegram bot/channel
  - Storage
    - [x] Add database schema migration tool
    - [x] SQLite DB backup to AWS S3
    - [x] Trade data store in SQLite DB
    - [ ] Base Database migrate from SQLite to Supabase(PostgreSQL)
- Bug Fix
  - [x] Trading signals error when double ma price are same

## Post

- [Serverless应用开发小记](https://www.bmpi.dev/dev/guide-to-serverless/)
- [Adventures in Serverless Application Development](https://www.bmpi.dev/en/dev/guide-to-serverless/)
