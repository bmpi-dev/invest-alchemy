-- liquibase formatted sql

-- changeset invest_alchemy:5

ALTER TABLE portfolio ADD portfolio_type VARCHAR(10) default 'private';
ALTER TABLE portfolio ADD portfolio_net_value float NOT NULL default 1.0;
ALTER TABLE portfolio ADD portfolio_trade_date VARCHAR(30) NOT NULL;
ALTER TABLE portfolio ADD portfolio_create_date VARCHAR(30) NOT NULL;

--rollback ALTER TABLE portfolio DROP COLUMN IF EXISTS portfolio_type;
--rollback ALTER TABLE portfolio DROP COLUMN IF EXISTS portfolio_net_value;
--rollback ALTER TABLE portfolio DROP COLUMN IF EXISTS portfolio_trade_date;
--rollback ALTER TABLE portfolio DROP COLUMN IF EXISTS portfolio_create_date;