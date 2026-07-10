-- =====================================================
-- FraudShield Index Creation Script
-- Project: AI-Based Mobile Money Fraud Risk Detection
-- Database: fraudshield
-- Purpose: Improve query performance for fraud monitoring
-- =====================================================


-- =====================================================
-- 1. CUSTOMER INDEXES
-- Speed up searches by customer code and phone number
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_customers_customer_code
ON customers(customer_code);

CREATE INDEX IF NOT EXISTS idx_customers_phone_number
ON customers(phone_number);

CREATE INDEX IF NOT EXISTS idx_customers_region
ON customers(region);


-- =====================================================
-- 2. ACCOUNT INDEXES
-- Speed up account lookup and customer-account joins
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_accounts_customer_id
ON accounts(customer_id);

CREATE INDEX IF NOT EXISTS idx_accounts_account_number
ON accounts(account_number);

CREATE INDEX IF NOT EXISTS idx_accounts_provider
ON accounts(provider);

CREATE INDEX IF NOT EXISTS idx_accounts_status
ON accounts(account_status);


-- =====================================================
-- 3. TRANSACTION INDEXES
-- Speed up transaction lookup, filtering, and joins
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_transactions_external_id
ON transactions(external_transaction_id);

CREATE INDEX IF NOT EXISTS idx_transactions_sender_account
ON transactions(sender_account_id);

CREATE INDEX IF NOT EXISTS idx_transactions_receiver_account
ON transactions(receiver_account_id);

CREATE INDEX IF NOT EXISTS idx_transactions_type
ON transactions(transaction_type);

CREATE INDEX IF NOT EXISTS idx_transactions_status
ON transactions(transaction_status);

CREATE INDEX IF NOT EXISTS idx_transactions_time
ON transactions(transaction_time);

CREATE INDEX IF NOT EXISTS idx_transactions_actual_fraud
ON transactions(is_actual_fraud);

CREATE INDEX IF NOT EXISTS idx_transactions_amount
ON transactions(amount);


-- =====================================================
-- 4. FRAUD PREDICTION INDEXES
-- Speed up fraud monitoring and model output queries
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_fraud_predictions_transaction_id
ON fraud_predictions(transaction_id);

CREATE INDEX IF NOT EXISTS idx_fraud_predictions_label
ON fraud_predictions(prediction_label);

CREATE INDEX IF NOT EXISTS idx_fraud_predictions_risk_level
ON fraud_predictions(risk_level);

CREATE INDEX IF NOT EXISTS idx_fraud_predictions_probability
ON fraud_predictions(fraud_probability);

CREATE INDEX IF NOT EXISTS idx_fraud_predictions_predicted_at
ON fraud_predictions(predicted_at);

CREATE INDEX IF NOT EXISTS idx_fraud_predictions_model_version
ON fraud_predictions(model_version);


-- =====================================================
-- 5. VERIFICATION REQUEST INDEXES
-- Speed up verification tracking
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_verification_transaction_id
ON verification_requests(transaction_id);

CREATE INDEX IF NOT EXISTS idx_verification_prediction_id
ON verification_requests(prediction_id);

CREATE INDEX IF NOT EXISTS idx_verification_status
ON verification_requests(verification_status);

CREATE INDEX IF NOT EXISTS idx_verification_channel
ON verification_requests(verification_channel);

CREATE INDEX IF NOT EXISTS idx_verification_created_at
ON verification_requests(created_at);


-- =====================================================
-- 6. AUDIT LOG INDEXES
-- Speed up system monitoring and traceability queries
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_audit_logs_event_type
ON audit_logs(event_type);

CREATE INDEX IF NOT EXISTS idx_audit_logs_entity_name
ON audit_logs(entity_name);

CREATE INDEX IF NOT EXISTS idx_audit_logs_action
ON audit_logs(action);

CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at
ON audit_logs(created_at);