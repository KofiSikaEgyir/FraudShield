-- =====================================================
-- FraudShield PaySim Staging Table Script
-- Project: AI-Based Mobile Money Fraud Risk Detection
-- Database: fraudshield
-- Purpose: Create raw staging table for PaySim dataset
-- =====================================================

DROP TABLE IF EXISTS paysim_staging;

CREATE TABLE paysim_staging (
    staging_id BIGSERIAL PRIMARY KEY,

    step INTEGER NOT NULL,

    transaction_type VARCHAR(30) NOT NULL,

    amount NUMERIC(18, 2) NOT NULL,

    name_orig VARCHAR(100) NOT NULL,

    oldbalance_org NUMERIC(18, 2) NOT NULL,

    newbalance_orig NUMERIC(18, 2) NOT NULL,

    name_dest VARCHAR(100) NOT NULL,

    oldbalance_dest NUMERIC(18, 2) NOT NULL,

    newbalance_dest NUMERIC(18, 2) NOT NULL,

    is_fraud SMALLINT NOT NULL CHECK (is_fraud IN (0, 1)),

    is_flagged_fraud SMALLINT NOT NULL CHECK (is_flagged_fraud IN (0, 1)),

    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);


-- Add helpful comments
COMMENT ON TABLE paysim_staging IS 'Raw staging table for PaySim mobile money-like transaction dataset.';

COMMENT ON COLUMN paysim_staging.step IS 'Time step from the PaySim simulation.';
COMMENT ON COLUMN paysim_staging.transaction_type IS 'Type of transaction such as CASH_OUT, TRANSFER, PAYMENT, CASH_IN, or DEBIT.';
COMMENT ON COLUMN paysim_staging.name_orig IS 'Original sender account identifier from PaySim.';
COMMENT ON COLUMN paysim_staging.name_dest IS 'Destination receiver account identifier from PaySim.';
COMMENT ON COLUMN paysim_staging.is_fraud IS 'Fraud label from PaySim: 1 means fraud, 0 means non-fraud.';
COMMENT ON COLUMN paysim_staging.is_flagged_fraud IS 'System flag label from PaySim.';