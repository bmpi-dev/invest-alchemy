-- liquibase formatted sql

-- changeset invest_alchemy:4

CREATE TABLE portfolio
(
  trader_username            VARCHAR(30),
  portfolio_name             VARCHAR(50) NOT NULL,
  comment                    text,
  portfolio_status           VARCHAR(10),
  portfolio_type             VARCHAR(10) default 'private',
  portfolio_net_value        float NOT NULL default 1.0,
  portfolio_trade_date       VARCHAR(30),
  portfolio_create_date      VARCHAR(30) NOT NULL,
  update_timestamp           timestamp without time zone default (now() at time zone 'utc'),
  create_timestamp           timestamp without time zone default (now() at time zone 'utc'),
  PRIMARY KEY (trader_username, portfolio_name)
);

--rollback DROP TABLE portfolio;