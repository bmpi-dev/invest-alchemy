-- liquibase formatted sql

-- changeset invest_alchemy:1

CREATE TABLE dma_trade_signal
(
  trade_date            TEXT NOT NULL,
  trade_code            TEXT NOT NULL,
  trade_name            TEXT,
  trade_type            VARCHAR(10),
  trade_timestamp       INTEGER DEFAULT (strftime('%s','now')),
  PRIMARY KEY (trade_date, trade_code)
);

--rollback DROP TABLE dma_trade_signal;