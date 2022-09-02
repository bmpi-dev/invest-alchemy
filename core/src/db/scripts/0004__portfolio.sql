-- liquibase formatted sql

-- changeset invest_alchemy:4

CREATE TABLE portfolio
(
  id                         serial PRIMARY KEY,
  trader_id                  int NOT NULL,
  portfolio_name             VARCHAR(50) NOT NULL,
  comment                    text,
  portfolio_status           VARCHAR(10),
  update_timestamp           timestamp without time zone default (now() at time zone 'utc'),
  create_timestamp           timestamp without time zone default (now() at time zone 'utc')
);

--rollback DROP TABLE portfolio;