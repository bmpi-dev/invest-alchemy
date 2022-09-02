-- liquibase formatted sql

-- changeset invest_alchemy:3

CREATE TABLE trader
(
  id                         serial PRIMARY KEY,
  username                   VARCHAR(30) UNIQUE,
  email                      VARCHAR(50),
  nickname                   VARCHAR(30),
  trader_type                VARCHAR(10),
  trader_status              VARCHAR(10),
  update_timestamp           timestamp without time zone default (now() at time zone 'utc'),
  create_timestamp           timestamp without time zone default (now() at time zone 'utc')
);

--rollback DROP TABLE trader;