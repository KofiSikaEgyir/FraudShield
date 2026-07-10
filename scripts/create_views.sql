-- =====================================================
-- FraudShield Analytical Views Script
-- Project: AI-Based Mobile Money Fraud Risk Detection
-- Database: fraudshield
-- Purpose: Create analytical views for fraud monitoring
-- =====================================================


-- =====================================================
-- 1. TRANSACTION PREDICTION SUMMARY VIEW
-- Combines transactions with fraud prediction results.
-- This is the main analytical view.
-- =====================================================

CREATE OR REPLACE VIEW vw_transaction_prediction_summary AS
SELECT
    t.transaction_id,
    t.external_transaction_id,
    t.transaction_type,
    t.amount,

    t.sender_account_id,
    sa.account_number AS sender_account_number,
    sc.customer_code AS sender_customer_code,
    sc.full_name AS sender_name,
    sc.phone_number AS sender_phone,
    sc.region AS sender_region,
    sc.district AS sender_district,

    t.receiver_account_id,
    ra.account_number AS receiver_account_number,
    rc.customer_code AS receiver_customer_code,
    rc.full_name AS receiver_name,
    rc.phone_number AS receiver_phone,

    t.sender_old_balance,
    t.sender_new_balance,
    t.receiver_old_balance,
    t.receiver_new_balance,

    t.transaction_channel,
    t.transaction_status,
    t.is_actual_fraud,
    t.transaction_time,

    fp.prediction_id,
    fp.model_name,
    fp.model_version,
    fp.prediction_label,
    fp.prediction_code,
    fp.fraud_probability,
    fp.risk_level,
    fp.top_risk_factors,
    fp.alert_message,
    fp.predicted_at

FROM transactions t
LEFT JOIN accounts sa
    ON t.sender_account_id = sa.account_id
LEFT JOIN customers sc
    ON sa.customer_id = sc.customer_id
LEFT JOIN accounts ra
    ON t.receiver_account_id = ra.account_id
LEFT JOIN customers rc
    ON ra.customer_id = rc.customer_id
LEFT JOIN fraud_predictions fp
    ON t.transaction_id = fp.transaction_id;


-- =====================================================
-- 2. HIGH RISK TRANSACTIONS VIEW
-- Shows transactions predicted as fraud or high risk.
-- =====================================================

CREATE OR REPLACE VIEW vw_high_risk_transactions AS
SELECT
    transaction_id,
    external_transaction_id,
    transaction_type,
    amount,
    sender_name,
    sender_phone,
    sender_region,
    sender_old_balance,
    sender_new_balance,
    prediction_label,
    fraud_probability,
    risk_level,
    alert_message,
    transaction_time
FROM vw_transaction_prediction_summary
WHERE prediction_label = 'Fraud'
   OR risk_level = 'High Risk'
ORDER BY fraud_probability DESC;


-- =====================================================
-- 3. DAILY FRAUD SUMMARY VIEW
-- Summarizes transactions and fraud predictions by day.
-- Useful for dashboards and monitoring.
-- =====================================================

CREATE OR REPLACE VIEW vw_daily_fraud_summary AS
SELECT
    DATE(transaction_time) AS transaction_date,

    COUNT(*) AS total_transactions,

    SUM(amount) AS total_transaction_value,

    COUNT(*) FILTER (
        WHERE prediction_label = 'Fraud'
    ) AS predicted_fraud_count,

    COUNT(*) FILTER (
        WHERE risk_level = 'High Risk'
    ) AS high_risk_count,

    COUNT(*) FILTER (
        WHERE is_actual_fraud = TRUE
    ) AS actual_fraud_count,

    ROUND(AVG(fraud_probability), 6) AS average_fraud_probability

FROM vw_transaction_prediction_summary
GROUP BY DATE(transaction_time)
ORDER BY transaction_date;


-- =====================================================
-- 4. TRANSACTION TYPE RISK SUMMARY VIEW
-- Shows fraud risk by transaction type.
-- Useful for explaining why TRANSFER and CASH_OUT matter.
-- =====================================================

CREATE OR REPLACE VIEW vw_transaction_type_risk_summary AS
SELECT
    transaction_type,

    COUNT(*) AS total_transactions,

    SUM(amount) AS total_transaction_value,

    COUNT(*) FILTER (
        WHERE prediction_label = 'Fraud'
    ) AS predicted_fraud_count,

    COUNT(*) FILTER (
        WHERE risk_level = 'High Risk'
    ) AS high_risk_count,

    COUNT(*) FILTER (
        WHERE is_actual_fraud = TRUE
    ) AS actual_fraud_count,

    ROUND(AVG(fraud_probability), 6) AS average_fraud_probability,

    ROUND(
        COUNT(*) FILTER (WHERE prediction_label = 'Fraud')::NUMERIC
        / NULLIF(COUNT(*), 0),
        6
    ) AS predicted_fraud_rate

FROM vw_transaction_prediction_summary
GROUP BY transaction_type
ORDER BY predicted_fraud_rate DESC, total_transaction_value DESC;


-- =====================================================
-- 5. CUSTOMER RISK PROFILE VIEW
-- Summarizes fraud risk at the customer level.
-- Useful for monitoring repeated suspicious activity.
-- =====================================================

CREATE OR REPLACE VIEW vw_customer_risk_profile AS
SELECT
    sender_customer_code AS customer_code,
    sender_name AS customer_name,
    sender_phone AS phone_number,
    sender_region AS region,
    sender_district AS district,

    COUNT(*) AS total_transactions,
    SUM(amount) AS total_transaction_value,

    COUNT(*) FILTER (
        WHERE prediction_label = 'Fraud'
    ) AS predicted_fraud_count,

    COUNT(*) FILTER (
        WHERE risk_level = 'High Risk'
    ) AS high_risk_count,

    ROUND(AVG(fraud_probability), 6) AS average_fraud_probability,

    MAX(transaction_time) AS last_transaction_time

FROM vw_transaction_prediction_summary
GROUP BY
    sender_customer_code,
    sender_name,
    sender_phone,
    sender_region,
    sender_district
ORDER BY high_risk_count DESC, average_fraud_probability DESC;


-- =====================================================
-- 6. MODEL PREDICTION PERFORMANCE VIEW
-- Compares actual fraud labels with model predictions.
-- This is useful when actual fraud labels are available.
-- =====================================================

CREATE OR REPLACE VIEW vw_model_prediction_performance AS
SELECT
    model_name,
    model_version,

    COUNT(*) AS total_predictions,

    COUNT(*) FILTER (
        WHERE prediction_code = 1
    ) AS predicted_fraud_count,

    COUNT(*) FILTER (
        WHERE prediction_code = 0
    ) AS predicted_non_fraud_count,

    COUNT(*) FILTER (
        WHERE is_actual_fraud = TRUE
    ) AS actual_fraud_count,

    COUNT(*) FILTER (
        WHERE prediction_code = 1 AND is_actual_fraud = TRUE
    ) AS true_positive,

    COUNT(*) FILTER (
        WHERE prediction_code = 1 AND is_actual_fraud = FALSE
    ) AS false_positive,

    COUNT(*) FILTER (
        WHERE prediction_code = 0 AND is_actual_fraud = TRUE
    ) AS false_negative,

    COUNT(*) FILTER (
        WHERE prediction_code = 0 AND is_actual_fraud = FALSE
    ) AS true_negative,

    ROUND(AVG(fraud_probability), 6) AS average_fraud_probability

FROM vw_transaction_prediction_summary
WHERE model_name IS NOT NULL
GROUP BY model_name, model_version;