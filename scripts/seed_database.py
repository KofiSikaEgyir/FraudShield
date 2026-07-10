# =====================================================
# FraudShield Seed Database Script
# Purpose: Insert sample records into PostgreSQL tables
# =====================================================

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


print("Seed database script is running...")


# Locate project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load .env file
load_dotenv(PROJECT_ROOT / ".env")

# Read database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found. Check your .env file.")


def seed_database():
    engine = create_engine(DATABASE_URL)

    with engine.begin() as connection:
        # Clear existing sample data
        connection.execute(text("""
            TRUNCATE TABLE
                verification_requests,
                fraud_predictions,
                transactions,
                accounts,
                customers,
                audit_logs
            RESTART IDENTITY CASCADE;
        """))

        # Insert customers
        connection.execute(text("""
            INSERT INTO customers
                (customer_code, full_name, phone_number, gender, region, district, kyc_level)
            VALUES
                ('CUS001', 'Kwame Mensah', '0240000001', 'Male', 'Greater Accra', 'Accra Metropolitan', 2),
                ('CUS002', 'Akosua Boateng', '0240000002', 'Female', 'Ashanti', 'Kumasi Metropolitan', 2),
                ('CUS003', 'Esi Amponsah', '0240000003', 'Female', 'Central', 'Cape Coast Metropolitan', 1);
        """))

        # Insert accounts
        connection.execute(text("""
            INSERT INTO accounts
                (customer_id, account_number, provider, account_type, current_balance, account_status)
            VALUES
                (1, 'MOMO001', 'MTN Mobile Money', 'Mobile Money', 5000.00, 'active'),
                (2, 'MOMO002', 'Telecel Cash', 'Mobile Money', 3000.00, 'active'),
                (3, 'MOMO003', 'AirtelTigo Money', 'Mobile Money', 1500.00, 'active');
        """))

        # Insert transactions
        connection.execute(text("""
            INSERT INTO transactions
                (
                    external_transaction_id,
                    sender_account_id,
                    receiver_account_id,
                    transaction_type,
                    amount,
                    sender_old_balance,
                    sender_new_balance,
                    receiver_old_balance,
                    receiver_new_balance,
                    transaction_channel,
                    transaction_status,
                    is_actual_fraud,
                    source_system
                )
            VALUES
                (
                    'TXN001',
                    1,
                    2,
                    'TRANSFER',
                    2500.00,
                    5000.00,
                    2500.00,
                    3000.00,
                    5500.00,
                    'APP',
                    'successful',
                    FALSE,
                    'Seed Data'
                ),
                (
                    'TXN002',
                    2,
                    3,
                    'CASH_OUT',
                    3000.00,
                    3000.00,
                    0.00,
                    1500.00,
                    1500.00,
                    'AGENT',
                    'successful',
                    TRUE,
                    'Seed Data'
                ),
                (
                    'TXN003',
                    3,
                    1,
                    'PAYMENT',
                    200.00,
                    1500.00,
                    1300.00,
                    2500.00,
                    2700.00,
                    'USSD',
                    'successful',
                    FALSE,
                    'Seed Data'
                );
        """))

        # Insert fraud predictions
        connection.execute(text("""
            INSERT INTO fraud_predictions
                (
                    transaction_id,
                    model_name,
                    model_version,
                    prediction_label,
                    prediction_code,
                    fraud_probability,
                    risk_level,
                    top_risk_factors,
                    alert_message
                )
            VALUES
                (
                    1,
                    'Random Forest',
                    'v1.0.0',
                    'Non-Fraud',
                    0,
                    0.120000,
                    'Low Risk',
                    '{"factors": ["normal transaction pattern"]}',
                    'Low Risk: This transaction does not show strong fraud indicators.'
                ),
                (
                    2,
                    'Random Forest',
                    'v1.0.0',
                    'Fraud',
                    1,
                    0.920000,
                    'High Risk',
                    '{"factors": ["CASH_OUT transaction", "sender balance reduced to zero", "high fraud probability"]}',
                    'High Risk Fraud Alert: This transaction appears suspicious. Pause and verify before proceeding.'
                ),
                (
                    3,
                    'Random Forest',
                    'v1.0.0',
                    'Non-Fraud',
                    0,
                    0.080000,
                    'Low Risk',
                    '{"factors": ["low transaction amount", "normal balance movement"]}',
                    'Low Risk: This transaction does not show strong fraud indicators.'
                );
        """))

        # Insert verification request
        connection.execute(text("""
            INSERT INTO verification_requests
                (
                    transaction_id,
                    prediction_id,
                    verification_channel,
                    recipient_phone,
                    verification_status,
                    verification_code,
                    response_notes
                )
            VALUES
                (
                    2,
                    2,
                    'SMS',
                    '0240000002',
                    'pending',
                    '123456',
                    'Verification request created for high-risk transaction.'
                );
        """))

        # Insert audit log
        connection.execute(text("""
            INSERT INTO audit_logs
                (event_type, entity_name, entity_id, action, performed_by, details)
            VALUES
                (
                    'DATABASE_SEED',
                    'all_tables',
                    NULL,
                    'Inserted sample FraudShield records',
                    'system',
                    '{"message": "Seed data inserted successfully"}'
                );
        """))

    print("Seed data inserted successfully.")


def show_table_counts():
    engine = create_engine(DATABASE_URL)

    tables = [
        "customers",
        "accounts",
        "transactions",
        "fraud_predictions",
        "verification_requests",
        "audit_logs"
    ]

    with engine.connect() as connection:
        print()
        print("Table record counts")
        print("-" * 30)

        for table in tables:
            result = connection.execute(
                text(f"SELECT COUNT(*) FROM {table};")
            )
            count = result.scalar()
            print(f"{table}: {count}")


if __name__ == "__main__":
    print("Starting database seeding...")
    seed_database()
    show_table_counts()
    print("Database seeding completed.")