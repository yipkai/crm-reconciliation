
import sqlite3
from pathlib import Path
import pandas as pd

# Locate the project directory
PROJECT_DIR = Path(__file__).resolve().parents[1]

# Define file paths
DATA_DIR = PROJECT_DIR / "data"
DB_PATH = PROJECT_DIR / "crm_reconciliation.db"

# Read the original CSV files
crm_df = pd.read_csv(DATA_DIR / "crm_customers.csv", dtype=str)
billing_df = pd.read_csv(DATA_DIR / "billing_contracts.csv", dtype=str)

print(f"CRM records loaded: {len(crm_df)}")
print(f"Billing records loaded: {len(billing_df)}")

# Connect to SQLite (creates the database if needed)
with sqlite3.connect(DB_PATH) as conn:

    # Load the raw data into SQL tables
    crm_df.to_sql(
        "raw_crm_customers",
        conn,
        if_exists="replace",
        index=False
    )

    billing_df.to_sql(
        "raw_billing_contracts",
        conn,
        if_exists="replace",
        index=False
    )

    # Verify the imported records
    crm_count = conn.execute(
        "SELECT COUNT(*) FROM raw_crm_customers"
    ).fetchone()[0]

    billing_count = conn.execute(
        "SELECT COUNT(*) FROM raw_billing_contracts"
    ).fetchone()[0]

print("\nDatabase created successfully.")
print(f"CRM records in SQL: {crm_count}")
print(f"Billing records in SQL: {billing_count}")
