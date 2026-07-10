# =====================================================
# FraudShield Database Connection Test
# Purpose: Test PostgreSQL connection using DATABASE_URL
# =====================================================

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Locate the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Load environment variables from .env
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path)


# Read DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not found. Check your .env file.")


def test_connection():
    try:
        # Create database engine
        engine = create_engine(DATABASE_URL)

        # Test connection
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT current_database(), current_user;")
            )

            database_name, database_user = result.fetchone()

            print("Database connection successful.")
            print(f"Connected database: {database_name}")
            print(f"Connected user: {database_user}")

    except Exception as error:
        print("Database connection failed.")
        print(f"Error: {error}")


if __name__ == "__main__":
    test_connection()