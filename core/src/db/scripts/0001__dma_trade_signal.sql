-- liquibase formatted sql

-- changeset invest_alchemy:1

CREATE TABLE dma_trade_signal
(
  trade_date            VARCHAR(30) NOT NULL,
  trade_code            VARCHAR(30) NOT NULL,
  trade_name            VARCHAR(50),
  trade_type            VARCHAR(20) NOT NULL,
  strategy_type         VARCHAR(20),
  trade_timestamp       timestamp without time zone default (now() at time zone 'utc'),
  PRIMARY KEY (trade_date, trade_code)
);

--rollback DROP TABLE dma_trade_signal;