# FraudShield: Mobile Money Fraud Detection and SMS Alert Prototype

FraudShield is an AI-based mobile money fraud risk detection and prevention prototype. The system uses machine learning to classify mobile money-like transactions as fraudulent or non-fraudulent, assigns a risk level, generates a fraud prevention alert message, simulates SMS notification for high-risk transactions, and stores prediction records in PostgreSQL for monitoring, auditing, and reporting.

This project was developed as part of the DMA898 Capstone Project for the MSc Data Management and Analytics programme at the University of Cape Coast.

---

## Project Title

**AI-Based Mobile Money Fraud Risk Detection and Prevention Framework Using Machine Learning and SMS Alert Simulation**

---

## Project Context

Mobile money is widely used in Ghana for transfers, payments, cash-out transactions, business transactions, remittances, and personal financial activity. However, fraud remains a major concern. Fraudsters commonly use fake calls, fake SMS alerts, impersonation, reversal scams, PIN requests, OTP requests, and pressure tactics to deceive customers.

FraudShield responds to this problem by combining machine learning fraud prediction with practical fraud prevention support. The system does not only predict whether a transaction is risky. It also generates an understandable alert message and simulates SMS notification for high-risk transactions.

---

## Main Objective

To develop an AI-based fraud detection and prevention prototype that detects suspicious mobile money-like transactions, generates fraud risk alerts, and simulates SMS notification for high-risk cases.

---

## Specific Objectives

1. Examine transaction patterns associated with mobile money fraud risk.
2. Build supervised machine learning models for fraud detection.
3. Compare model performance using fraud-sensitive evaluation metrics.
4. Select the best-performing model for deployment.
5. Generate understandable fraud alert messages from model outputs.
6. Build a FastAPI prototype for live transaction scoring.
7. Save prediction and SMS alert records in PostgreSQL.
8. Demonstrate simulated SMS alerting for high-risk transactions.

---

## Dataset

The project uses the **PaySim dataset**, a synthetic mobile money-like transaction dataset commonly used for fraud detection research.

Real mobile money transaction data is difficult to access because of privacy, confidentiality, and regulatory restrictions. PaySim provides a useful substitute for developing and testing a fraud detection framework.

### Dataset Summary

| Item | Value |
|---|---:|
| Total records | 6,362,620 |
| Fraud records | 8,213 |
| Non-fraud records | 6,354,407 |
| Fraud rate | 0.1291% |
| Target variable | `isFraud` |

### Fraud by Transaction Type

| Transaction Type | Total Transactions | Fraud Count | Fraud Rate |
|---|---:|---:|---:|
| CASH_OUT | 2,237,500 | 4,116 | 0.001840 |
| TRANSFER | 532,909 | 4,097 | 0.007688 |
| CASH_IN | 1,399,284 | 0 | 0.000000 |
| DEBIT | 41,432 | 0 | 0.000000 |
| PAYMENT | 2,151,495 | 0 | 0.000000 |

Fraud appears only in `CASH_OUT` and `TRANSFER` transactions in the PaySim dataset.

---

## Machine Learning Models

Four models were developed and compared:

1. Logistic Regression
2. Decision Tree
3. Random Forest
4. XGBoost

Because fraud cases are rare, accuracy alone was not used as the main basis for model selection. Greater attention was given to recall, precision, F1-score, ROC-AUC, and especially PR-AUC.

### Final Model Comparison

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9415 | 0.0198 | 0.9152 | 0.0388 | 0.9854 | 0.4746 |
| Decision Tree | 0.9942 | 0.1811 | 0.9842 | 0.3059 | 0.9918 | 0.7777 |
| Random Forest | 0.9958 | 0.2331 | 0.9923 | 0.3776 | 0.9984 | 0.8942 |
| XGBoost | 0.9909 | 0.1235 | 0.9963 | 0.2197 | 0.9989 | 0.8145 |

The final selected model is **Random Forest** because it achieved the best overall operational balance, especially in terms of PR-AUC, F1-score, precision, and recall.

---

## Selected Model

**Random Forest** was selected as the final model.

### Random Forest Test Performance

| Metric | Value |
|---|---:|
| Accuracy | 0.9958 |
| Precision | 0.2331 |
| Recall | 0.9923 |
| F1-score | 0.3776 |
| ROC-AUC | 0.9984 |
| PR-AUC | 0.8942 |

### Random Forest Confusion Matrix

|  | Predicted Non-Fraud | Predicted Fraud |
|---|---:|---:|
| Actual Non-Fraud | 1,898,280 | 8,042 |
| Actual Fraud | 19 | 2,445 |

The Random Forest model correctly detected 2,445 fraud cases and missed only 19 fraud cases in the test set.

---

## Important Features

The most important Random Forest features were:

| Feature | Importance |
|---|---:|
| `oldbalanceOrg` | 0.3849 |
| `amount` | 0.2507 |
| `newbalanceOrig` | 0.1625 |
| `type_TRANSFER` | 0.1085 |
| `type_PAYMENT` | 0.0563 |
| `type_CASH_OUT` | 0.0365 |
| `type_DEBIT` | 0.0005 |

The model relied mainly on sender old balance, transaction amount, sender new balance, and transaction type.

---

## System Architecture

The project has evolved from notebook-based modelling into a database-backed API prototype.

```text
Transaction Input
       ↓
FastAPI /predict/
       ↓
Saved Random Forest Model
       ↓
Fraud Prediction + Probability
       ↓
Risk Level Assignment
       ↓
Fraud Alert Message
       ↓
SMS Simulation for High-Risk Cases
       ↓
PostgreSQL Prediction and SMS Log
       ↓
History, High-Risk, and Summary Endpoints
```

---

## Technology Stack

| Component | Tool |
|---|---|
| Programming Language | Python |
| Machine Learning | scikit-learn |
| Model Storage | joblib |
| API Framework | FastAPI |
| API Server | Uvicorn |
| Database | PostgreSQL |
| Database Tool | pgAdmin |
| Data Processing | pandas, SQL |
| SMS Layer | Simulated SMS service |
| Version Control | Git and GitHub |
| Development Environment | Positron |

---

## Project Structure

```text
FraudShield/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── prediction_routes.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── prediction_schema.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── database_service.py
│   │   │   ├── fraud_model_service.py
│   │   │   └── sms_service.py
│   │   │
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── PaySim.csv
│   └── processed/
│       └── paysim_ml_features.csv
│
├── docs/
│
├── model/
│   ├── amount_95th.pkl
│   ├── api_input_features.json
│   └── random_forest_fraud_model.pkl
│
├── notebooks/
│
├── outputs/
│
├── scripts/
│   ├── alter_api_prediction_logs_add_sms_fields.sql
│   ├── create_api_prediction_logs_table.sql
│   ├── create_indexes.sql
│   ├── create_paysim_analytical_views.sql
│   ├── create_paysim_indexes.sql
│   ├── create_paysim_staging_table.sql
│   ├── create_tables.sql
│   ├── create_views.sql
│   ├── export_ml_features.py
│   ├── load_paysim.py
│   ├── seed_database.py
│   ├── test_db_connection.py
│   └── test_fraudshield_api_demo.py
│
├── .env
├── .gitignore
└── README.md
```

---

## Environment Setup

This project requires **Python 3.12** because the saved Random Forest model was trained using `scikit-learn==1.5.1`.

### Create Virtual Environment

```powershell
py -3.12 -m venv .venv312
```

### Activate Virtual Environment

```powershell
.\.venv312\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r backend/requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/fraudshield

APP_NAME=FraudShield
APP_ENV=development
SECRET_KEY=ReplaceThisWithAStrongRandomSecret
MODEL_VERSION=v1.0.0
```

Replace `YOUR_PASSWORD` with your actual PostgreSQL password.

Do not push `.env` to GitHub.

---

## PostgreSQL Database

Database name:

```text
fraudshield
```

The database includes both operational and analytical tables.

| Table | Purpose |
|---|---|
| `customers` | Customer information |
| `accounts` | Mobile money account details |
| `transactions` | Transaction records |
| `fraud_predictions` | Model prediction outputs |
| `verification_requests` | Verification actions |
| `audit_logs` | System audit records |
| `paysim_staging` | Raw PaySim data |
| `api_prediction_logs` | API prediction and SMS alert logs |

---

## Important Database and Processing Scripts

Run the SQL scripts in PostgreSQL using pgAdmin or `psql`.

```powershell
psql -U postgres -d fraudshield -f scripts/create_tables.sql
psql -U postgres -d fraudshield -f scripts/create_indexes.sql
psql -U postgres -d fraudshield -f scripts/create_views.sql
psql -U postgres -d fraudshield -f scripts/create_paysim_staging_table.sql
psql -U postgres -d fraudshield -f scripts/create_paysim_analytical_views.sql
psql -U postgres -d fraudshield -f scripts/create_paysim_indexes.sql
psql -U postgres -d fraudshield -f scripts/create_api_prediction_logs_table.sql
psql -U postgres -d fraudshield -f scripts/alter_api_prediction_logs_add_sms_fields.sql
```

Run Python scripts with Python:

```powershell
python scripts/test_db_connection.py
python scripts/seed_database.py
python scripts/load_paysim.py
python scripts/export_ml_features.py
```

---

## API Endpoints

Start the FastAPI server:

```powershell
python -m uvicorn backend.app.main:app --reload
```

Open the documentation page:

```text
http://127.0.0.1:8000/docs
```

### Available Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Root endpoint |
| GET | `/health` | Check API health |
| POST | `/predict/` | Predict fraud risk and simulate SMS if high risk |
| GET | `/predict/history` | Retrieve recent prediction logs |
| GET | `/predict/high-risk` | Retrieve high-risk prediction logs |
| GET | `/predict/summary` | Retrieve prediction and SMS summary |

---

## Sample API Request

Endpoint:

```text
POST /predict/
```

Example high-risk request:

```json
{
  "customer_phone": "0240000001",
  "type": "TRANSFER",
  "amount": 250000,
  "oldbalanceOrg": 250000,
  "newbalanceOrig": 0
}
```

Example high-risk response:

```json
{
  "log_id": 8,
  "prediction": "Fraud",
  "prediction_code": 1,
  "fraud_probability": 0.9865,
  "risk_level": "High Risk",
  "alert_message": "High Risk Fraud Alert: This transaction appears suspicious because the transaction type is commonly associated with fraud risk, and the sender's balance was reduced to zero after the transaction. Pause before proceeding. Confirm the recipient, amount, and transaction purpose. Do not share your PIN or OTP with anyone.",
  "sms_required": true,
  "sms_status": "simulated",
  "sms_message": "FraudShield Alert: A High Risk TRANSFER transaction of GHS 250,000.00 was detected with fraud probability 0.9865. Do not share your PIN or OTP. If you did not authorize this transaction, contact your provider immediately.",
  "sms_provider": "Simulation"
}
```

Example low-risk request:

```json
{
  "customer_phone": "0240000002",
  "type": "PAYMENT",
  "amount": 100,
  "oldbalanceOrg": 5000,
  "newbalanceOrig": 4900
}
```

Expected low-risk SMS result:

```json
{
  "sms_required": false,
  "sms_status": "not_required",
  "sms_message": null,
  "sms_provider": "Simulation"
}
```

---

## SMS Alert Simulation

The current version uses a simulated SMS service.

For high-risk transactions:

```text
sms_required = true
sms_status = simulated
```

For low-risk transactions:

```text
sms_required = false
sms_status = not_required
```

The SMS simulation exists because live SMS requires an external SMS provider such as Twilio, Hubtel, Mnotify, Nalo Solutions, or Africa’s Talking.

Future versions can replace the simulation service with a real SMS gateway.

---

## Demo Script

The project includes a demo script for testing the API.

Make sure the server is running first:

```powershell
python -m uvicorn backend.app.main:app --reload
```

Then open a second terminal and run:

```powershell
python scripts/test_fraudshield_api_demo.py
```

The script tests:

1. Health endpoint
2. High-risk transaction with SMS simulation
3. Low-risk transaction with no SMS required
4. Prediction history endpoint
5. High-risk logs endpoint
6. Prediction summary endpoint

---

## Current Prototype Capabilities

FraudShield currently supports:

- Fraud prediction using Random Forest
- Fraud probability scoring
- Risk level assignment
- Fraud prevention alert message generation
- Simulated SMS alert for high-risk transactions
- No SMS alert for low-risk transactions
- PostgreSQL prediction and SMS logging
- Prediction history retrieval
- High-risk prediction retrieval
- Dashboard-style prediction and SMS summary
- Full API demo testing through a script

---

## Current Limitations

1. The dataset is synthetic and not real Ghanaian mobile money transaction data.
2. SMS alerts are simulated and are not yet sent through a live SMS gateway.
3. The current API input is simplified and does not yet include full customer, account, device, location, or receiver details.
4. The system is a prototype and has not been deployed to a public server.
5. False positives remain a concern in real fraud detection systems and would require careful operational review.
6. Real deployment would require collaboration with mobile money operators, banks, fintechs, or regulators.

---

## Future Improvements

Future development can include:

- Live SMS integration using Twilio, Hubtel, Mnotify, Nalo Solutions, or Africa’s Talking
- Dashboard interface for fraud monitoring
- User authentication and admin access control
- Customer verification workflow
- Integration with real anonymized transaction data
- Model retraining pipeline
- Real-time deployment using cloud hosting
- More advanced explainability using SHAP or LIME
- Improved fraud investigation workflow
- Integration with telecom or banking transaction systems

---

## Author

**Philip Kofi Sika Egyir**  
MSc Data Management and Analytics  
Department of Data Science and Economic Policy  
University of Cape Coast  
Index Number: SE/DAT/25/0016

---

## Project Status

Current status:

```text
Working prototype completed
FastAPI model endpoint completed
PostgreSQL logging completed
SMS simulation completed
API demo script completed
Documentation in progress
```