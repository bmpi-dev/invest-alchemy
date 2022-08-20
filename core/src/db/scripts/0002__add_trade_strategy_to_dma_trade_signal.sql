-- liquibase formatted sql

-- changeset invest_alchemy:2

ALTER TABLE dma_trade_signal ADD trade_strategy TEXT DEFAULT '11/22';

--rollback ALTER TABLE dma_trade_signal DROP trade_strategy;