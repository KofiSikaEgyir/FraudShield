-- =====================================================
-- FraudShield SMS Alert Fields
-- Project: Mobile Money Fraud Detection
-- Purpose: Add SMS alert tracking fields to API logs
-- =====================================================

ALTER TABLE api_prediction_logs
ADD COLUMN IF NOT EXISTS customer_phone VARCHAR(20);

ALTER TABLE api_prediction_logs
ADD COLUMN IF NOT EXISTS sms_required BOOLEAN DEFAULT FALSE;

ALTER TABLE api_prediction_logs
ADD COLUMN IF NOT EXISTS sms_status VARCHAR(30) DEFAULT 'not_required'
    CHECK (sms_status IN ('not_required', 'simulated', 'sent', 'failed'));

ALTER TABLE api_prediction_logs
ADD COLUMN IF NOT EXISTS sms_message TEXT;

ALTER TABLE api_prediction_logs
ADD COLUMN IF NOT EXISTS sms_provider VARCHAR(50) DEFAULT 'Simulation';

ALTER TABLE api_prediction_logs
ADD COLUMN IF NOT EXISTS sms_sent_at TIMESTAMPTZ;

ALTER TABLE api_prediction_logs
ADD COLUMN IF NOT EXISTS sms_error TEXT;


-- Helpful indexes for SMS monitoring
CREATE INDEX IF NOT EXISTS idx_api_prediction_logs_customer_phone
ON api_prediction_logs(customer_phone);

CREATE INDEX IF NOT EXISTS idx_api_prediction_logs_sms_status
ON api_prediction_logs(sms_status);

CREATE INDEX IF NOT EXISTS idx_api_prediction_logs_sms_required
ON api_prediction_logs(sms_required);


COMMENT ON COLUMN api_prediction_logs.customer_phone IS
'Phone number that receives the fraud alert SMS.';

COMMENT ON COLUMN api_prediction_logs.sms_required IS
'Indicates whether SMS alert was required for the prediction.';

COMMENT ON COLUMN api_prediction_logs.sms_status IS
'SMS delivery status such as not_required, simulated, sent, or failed.';

COMMENT ON COLUMN api_prediction_logs.sms_message IS
'Fraud alert SMS message generated for the customer.';

COMMENT ON COLUMN api_prediction_logs.sms_provider IS
'SMS provider used, for example Simulation, Twilio, Hubtel, or Mnotify.';

COMMENT ON COLUMN api_prediction_logs.sms_sent_at IS
'Timestamp when SMS alert was sent or simulated.';

COMMENT ON COLUMN api_prediction_logs.sms_error IS
'Error message if SMS sending failed.';