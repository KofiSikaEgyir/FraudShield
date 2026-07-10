-- =====================================================
-- FraudShield PaySim Analytical Views Script
-- Project: AI-Based Mobile Money Fraud Risk Detection
-- Database: fraudshield
-- Purpose: Create analytical views for PaySim fraud analysis
-- =====================================================


-- =====================================================
-- 1. PAYSIM DATASET SUMMARY VIEW
-- Gives overall dataset size and fraud distribution.
-- =====================================================

CREATE OR REPLACE VIEW vw_paysim_dataset_summary AS
SELECT
    COUNT(*) AS total_records,

    COUNT(*) FILTER (
        WHERE is_fraud = 1
    ) AS fraud_records,

    COUNT(*) FILTER (
        WHERE is_fraud = 0
    ) AS non_fraud_records,

    ROUND(
        COUNT(*) FILTER (WHERE is_fraud = 1)::NUMERIC
        / NULLIF(COUNT(*), 0),
        6
    ) AS fraud_rate,

    MIN(amount) AS minimum_amount,
    MAX(amount) AS maximum_amount,
    ROUND(AVG(amount), 2) AS average_amount

FROM paysim_staging;


-- =====================================================
-- 2. FRAUD BY TRANSACTION TYPE VIEW
-- Shows where fraud occurs across transaction types.
-- =====================================================

CREATE OR REPLACE VIEW vw_paysim_fraud_by_transaction_type AS
SELECT
    transaction_type,

    COUNT(*) AS total_transactions,

    COUNT(*) FILTER (
        WHERE is_fraud = 1
    ) AS fraud_count,

    COUNT(*) FILTER (
        WHERE is_fraud = 0
    ) AS non_fraud_count,

    ROUND(
        COUNT(*) FILTER (WHERE is_fraud = 1)::NUMERIC
        / NULLIF(COUNT(*), 0),
        6
    ) AS fraud_rate,

    ROUND(AVG(amount), 2) AS average_amount,
    MIN(amount) AS minimum_amount,
    MAX(amount) AS maximum_amount

FROM paysim_staging
GROUP BY transaction_type
ORDER BY fraud_count DESC, fraud_rate DESC;


-- =====================================================
-- 3. FRAUD AMOUNT SUMMARY VIEW
-- Compares transaction amount patterns by fraud label.
-- =====================================================

CREATE OR REPLACE VIEW vw_paysim_amount_summary_by_fraud AS
SELECT
    is_fraud,

    CASE
        WHEN is_fraud = 1 THEN 'Fraud'
        ELSE 'Non-Fraud'
    END AS fraud_label,

    COUNT(*) AS total_transactions,

    MIN(amount) AS minimum_amount,
    MAX(amount) AS maximum_amount,
    ROUND(AVG(amount), 2) AS average_amount,

    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY amount) AS amount_25th_percentile,
    PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY amount) AS amount_median,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY amount) AS amount_75th_percentile,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY amount) AS amount_95th_percentile

FROM paysim_staging
GROUP BY is_fraud
ORDER BY is_fraud DESC;


-- =====================================================
-- 4. BALANCE ERROR FEATURES VIEW
-- Creates balance movement and inconsistency features.
-- These are important for fraud-risk analysis.
-- =====================================================

CREATE OR REPLACE VIEW vw_paysim_balance_error_features AS
SELECT
    staging_id,
    step,
    transaction_type,
    amount,

    name_orig,
    oldbalance_org,
    newbalance_orig,

    name_dest,
    oldbalance_dest,
    newbalance_dest,

    is_fraud,
    is_flagged_fraud,

    (oldbalance_org - newbalance_orig) AS sender_balance_change,

    (newbalance_dest - oldbalance_dest) AS receiver_balance_change,

    ABS(amount - (oldbalance_org - newbalance_orig)) AS abs_sender_balance_error,

    ABS(amount - (newbalance_dest - oldbalance_dest)) AS abs_receiver_balance_error,

    CASE
        WHEN oldbalance_org > 0 AND newbalance_orig = 0 THEN 1
        ELSE 0
    END AS sender_balance_zero_after_transaction,

    CASE
        WHEN transaction_type IN ('TRANSFER', 'CASH_OUT') THEN 1
        ELSE 0
    END AS risky_transaction_type

FROM paysim_staging;


-- =====================================================
-- 5. BALANCE ERROR SUMMARY BY FRAUD VIEW
-- Summarizes engineered balance features by fraud label.
-- =====================================================

CREATE OR REPLACE VIEW vw_paysim_balance_error_summary_by_fraud AS
SELECT
    is_fraud,

    CASE
        WHEN is_fraud = 1 THEN 'Fraud'
        ELSE 'Non-Fraud'
    END AS fraud_label,

    COUNT(*) AS total_transactions,

    ROUND(AVG(sender_balance_change), 2) AS avg_sender_balance_change,
    ROUND(AVG(receiver_balance_change), 2) AS avg_receiver_balance_change,

    ROUND(AVG(abs_sender_balance_error), 2) AS avg_abs_sender_balance_error,
    ROUND(AVG(abs_receiver_balance_error), 2) AS avg_abs_receiver_balance_error,

    COUNT(*) FILTER (
        WHERE sender_balance_zero_after_transaction = 1
    ) AS sender_zero_balance_count,

    ROUND(
        COUNT(*) FILTER (WHERE sender_balance_zero_after_transaction = 1)::NUMERIC
        / NULLIF(COUNT(*), 0),
        6
    ) AS sender_zero_balance_rate

FROM vw_paysim_balance_error_features
GROUP BY is_fraud
ORDER BY is_fraud DESC;


-- =====================================================
-- 6. PAYSIM ML FEATURES VIEW
-- Creates a clean feature view for modelling or reporting.
-- This mirrors the features used in the machine learning workflow.
-- =====================================================

CREATE OR REPLACE VIEW vw_paysim_ml_features AS
SELECT
    staging_id,

    step,
    transaction_type,
    amount,

    oldbalance_org,
    newbalance_orig,
    oldbalance_dest,
    newbalance_dest,

    sender_balance_change,
    receiver_balance_change,
    abs_sender_balance_error,
    abs_receiver_balance_error,

    sender_balance_zero_after_transaction,
    risky_transaction_type,

    is_fraud,
    is_flagged_fraud

FROM vw_paysim_balance_error_features;


-- =====================================================
-- 7. PAYSIM STEP FRAUD TREND VIEW
-- Summarizes fraud activity by PaySim simulation step.
-- Useful for time-based monitoring.
-- =====================================================

CREATE OR REPLACE VIEW vw_paysim_step_fraud_trend AS
SELECT
    step,

    COUNT(*) AS total_transactions,

    COUNT(*) FILTER (
        WHERE is_fraud = 1
    ) AS fraud_count,

    COUNT(*) FILTER (
        WHERE is_fraud = 0
    ) AS non_fraud_count,

    ROUND(
        COUNT(*) FILTER (WHERE is_fraud = 1)::NUMERIC
        / NULLIF(COUNT(*), 0),
        6
    ) AS fraud_rate,

    SUM(amount) AS total_transaction_value,
    ROUND(AVG(amount), 2) AS average_transaction_amount

FROM paysim_staging
GROUP BY step
ORDER BY step;