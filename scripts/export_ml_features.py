# =====================================================
# FraudShield ML Feature Export Script
# Purpose: Export ML-ready PaySim features from PostgreSQL
# Method: Memory-safe PostgreSQL COPY streaming
# =====================================================

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


print("ML feature export script is running...")


# Locate project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load .env file
load_dotenv(PROJECT_ROOT / ".env")

# Read database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found. Check your .env file.")


# Define output path
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "paysim_ml_features.csv"

# Make sure processed folder exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def export_ml_features():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        print("Exporting ML-ready features from PostgreSQL...")
        print("This may take some time because the dataset has over 6.3 million rows.")

        export_query = """
            COPY (
                SELECT
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
                FROM vw_paysim_ml_features
            )
            TO STDOUT
            WITH CSV HEADER;
        """

        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as file:
            cursor.copy_expert(export_query, file)

        print("ML features exported successfully.")
        print(f"Output file: {OUTPUT_FILE}")

        # Verification from database
        cursor.execute("SELECT COUNT(*) FROM vw_paysim_ml_features;")
        total_rows = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM vw_paysim_ml_features WHERE is_fraud = 1;")
        fraud_rows = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM vw_paysim_ml_features WHERE is_fraud = 0;")
        non_fraud_rows = cursor.fetchone()[0]

        print()
        print("Exported ML feature summary")
        print("-" * 40)
        print(f"Rows: {total_rows:,}")
        print("Columns: 15")
        print(f"Fraud records: {fraud_rows:,}")
        print(f"Non-fraud records: {non_fraud_rows:,}")

    except Exception as error:
        print("ML feature export failed.")
        print(f"Error: {error}")

    finally:
        if "cursor" in locals():
            cursor.close()

        if "conn" in locals():
            conn.close()


if __name__ == "__main__":
    export_ml_features()