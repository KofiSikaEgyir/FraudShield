# FraudShield Demo Guide

This guide explains how to demonstrate the FraudShield prototype during the final project presentation or defense.

---

## 1. Open the Project Folder

Open PowerShell or the terminal in the project folder:

```powershell
cd C:\Users\kofis\Desktop\FraudShield
```

---

## 2. Activate the Virtual Environment

```powershell
.\.venv312\Scripts\Activate.ps1
```

The terminal should show:

```text
(.venv312)
```

---

## 3. Start the FastAPI Server

```powershell
python -m uvicorn backend.app.main:app --reload
```

Expected server address:

```text
http://127.0.0.1:8000
```

---

## 4. Open the API Documentation

Open this URL in the browser:

```text
http://127.0.0.1:8000/docs
```

Use this to show the available API endpoints.

Important endpoints:

| Endpoint | Purpose |
|---|---|
| `/health` | Checks system health |
| `/predict/` | Predicts fraud risk |
| `/predict/history` | Shows recent prediction logs |
| `/predict/high-risk` | Shows high-risk fraud logs |
| `/predict/summary` | Shows prediction and SMS summary |

---

## 5. Open the FraudShield Dashboard

Open this URL:

```text
http://127.0.0.1:8000/static/dashboard.html
```

The dashboard shows:

- Summary cards
- Transaction prediction form
- Recent prediction history
- High-risk SMS alert logs

---

## 6. High-Risk Demo Case

Use the following input on the dashboard:

| Field | Value |
|---|---|
| Customer Phone | `0240000001` |
| Transaction Type | `TRANSFER` |
| Amount | `250000` |
| Old Balance | `250000` |
| New Balance | `0` |

Expected result:

```text
Prediction: Fraud
Risk Level: High Risk
Fraud Probability: 0.9865
SMS Required: true
SMS Status: simulated
```

Expected SMS message:

```text
FraudShield Alert: A High Risk TRANSFER transaction of GHS 250,000.00 was detected with fraud probability 0.9865. Do not share your PIN or OTP. If you did not authorize this transaction, contact your provider immediately.
```

Explanation:

This transaction is risky because it is a transfer transaction, the amount is high, and the sender’s balance becomes zero after the transaction. The system therefore classifies it as high risk and simulates an SMS fraud alert.

---

## 7. Low-Risk Demo Case

Use the following input on the dashboard:

| Field | Value |
|---|---|
| Customer Phone | `0240000002` |
| Transaction Type | `PAYMENT` |
| Amount | `100` |
| Old Balance | `5000` |
| New Balance | `4900` |

Expected result:

```text
Prediction: Non-Fraud
Risk Level: Low Risk
Fraud Probability: 0.0000
SMS Required: false
SMS Status: not_required
```

Explanation:

This transaction is a normal low-value payment. The model does not identify strong fraud indicators, so no SMS alert is required.

---

## 8. Show PostgreSQL Logging

In pgAdmin, run:

```sql
SELECT
    log_id,
    customer_phone,
    transaction_type,
    amount,
    prediction_label,
    risk_level,
    fraud_probability,
    sms_required,
    sms_status,
    sms_message,
    sms_provider,
    created_at
FROM api_prediction_logs
ORDER BY log_id DESC
LIMIT 10;
```

Use this to show that every prediction is stored in PostgreSQL.

---

## 9. Show Summary Endpoint

Open:

```text
http://127.0.0.1:8000/predict/summary
```

This shows:

- Total predictions
- Fraud predictions
- Non-fraud predictions
- High-risk predictions
- Low-risk predictions
- SMS required count
- SMS simulated count
- SMS failed count
- Latest prediction time
- Latest SMS alert time

---

## 10. Optional Demo Script

The project also includes a command-line demo script.

Start the FastAPI server first, then open another terminal and run:

```powershell
python scripts/test_fraudshield_api_demo.py
```

This script tests:

1. Health endpoint
2. High-risk fraud prediction
3. Low-risk prediction
4. Prediction history
5. High-risk logs
6. Summary endpoint

---

## 11. Key Presentation Explanation

During the presentation, explain the system flow as:

```text
Transaction Input
      ↓
FastAPI Backend
      ↓
Random Forest Fraud Model
      ↓
Fraud Probability and Risk Level
      ↓
Fraud Alert Message
      ↓
Simulated SMS Alert for High-Risk Transactions
      ↓
PostgreSQL Logging
      ↓
Dashboard and API Monitoring
```

---

## 12. Important Limitation to Mention

The SMS service is simulated in the current prototype. No real SMS is sent.

This is because live SMS delivery requires integration with an external SMS gateway such as Twilio, Hubtel, Mnotify, Nalo Solutions, or Africa’s Talking.

The simulation demonstrates how the alert workflow will behave before live SMS integration.

---

## 13. Strong Closing Statement

FraudShield demonstrates how machine learning can support mobile money fraud prevention by detecting risky transactions, generating understandable fraud alerts, simulating SMS notifications, and storing prediction logs for monitoring and investigation.