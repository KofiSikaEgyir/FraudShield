-- =====================================================
-- FraudShield PaySim Index Creation Script
-- Project: AI-Based Mobile Money Fraud Risk Detection
-- Database: fraudshield
-- Purpose: Improve query speed on PaySim staging data
-- =====================================================


-- =====================================================
-- 1. BASIC LOOKUP INDEXES
-- Useful for filtering by transaction type and fraud label
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_paysim_transaction_type
ON paysim_staging(transaction_type);

CREATE INDEX IF NOT EXISTS idx_paysim_is_fraud
ON paysim_staging(is_fraud);

CREATE INDEX IF NOT EXISTS idx_paysim_is_flagged_fraud
ON paysim_staging(is_flagged_fraud);

CREATE INDEX IF NOT EXISTS idx_paysim_step
ON paysim_staging(step);


-- =====================================================
-- 2. ACCOUNT IDENTIFIER INDEXES
-- Useful for sender and receiver transaction history
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_paysim_name_orig
ON paysim_staging(name_orig);

CREATE INDEX IF NOT EXISTS idx_paysim_name_dest
ON paysim_staging(name_dest);


-- =====================================================
-- 3. AMOUNT AND BALANCE INDEXES
-- Useful for amount-based and balance-based analysis
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_paysim_amount
ON paysim_staging(amount);

CREATE INDEX IF NOT EXISTS idx_paysim_oldbalance_org
ON paysim_staging(oldbalance_org);

CREATE INDEX IF NOT EXISTS idx_paysim_newbalance_orig
ON paysim_staging(newbalance_orig);

CREATE INDEX IF NOT EXISTS idx_paysim_oldbalance_dest
ON paysim_staging(oldbalance_dest);

CREATE INDEX IF NOT EXISTS idx_paysim_newbalance_dest
ON paysim_staging(newbalance_dest);


-- =====================================================
-- 4. COMPOSITE INDEXES
-- Useful for common fraud analysis queries
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_paysim_type_fraud
ON paysim_staging(transaction_type, is_fraud);

CREATE INDEX IF NOT EXISTS idx_paysim_step_fraud
ON paysim_staging(step, is_fraud);

CREATE INDEX IF NOT EXISTS idx_paysim_orig_fraud
ON paysim_staging(name_orig, is_fraud);

CREATE INDEX IF NOT EXISTS idx_paysim_dest_fraud
ON paysim_staging(name_dest, is_fraud);


-- =====================================================
-- 5. ANALYZE TABLE
-- Updates PostgreSQL statistics for better query planning
-- =====================================================

ANALYZE paysim_staging;