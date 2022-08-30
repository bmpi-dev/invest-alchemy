-- liquibase formatted sql

-- changeset invest_alchemy:2

CREATE TABLE index_daily
(
  trade_date            VARCHAR(30) NOT NULL,
  trade_code            VARCHAR(30) NOT NULL,
  trade_name            VARCHAR(50),
  open_price            float NOT NULL,
  close_price           float NOT NULL,
  high_price            float NOT NULL,
  low_price             float NOT NULL,
  change                float NOT NULL,
  pct_chg               float NOT NULL,
  trade_timestamp       timestamp without time zone default (now() at time zone 'utc'),
  PRIMARY KEY (trade_date, trade_code)
);

--rollback DROP TABLE index_daily;