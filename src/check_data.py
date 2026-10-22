
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "crm_reconciliation.db"

with sqlite3.connect(DB_PATH) as conn:

    # Check 1: Missing email addresses
    print("\n--- CUSTOMERS WITH MISSING EMAILS ---")

    query = """
    SELECT customer_id, customer_name, email
    FROM raw_crm_customers
    WHERE email IS NULL OR TRIM(email) = ''
    """

    for row in conn.execute(query):
        print(row)

    # Check 2: Duplicate email addresses
    print("\n--- DUPLICATE EMAIL ADDRESSES ---")

    query = """
    SELECT LOWER(TRIM(email)) AS normalized_email,
           COUNT(*) AS occurrences
    FROM raw_crm_customers
    WHERE email IS NOT NULL AND TRIM(email) != ''
    GROUP BY LOWER(TRIM(email))
    HAVING COUNT(*) > 1
    """

    for row in conn.execute(query):
        print(row)

    # Check 3: Invoice discrepancies
    print("\n--- CONTRACT / INVOICE DISCREPANCIES ---")

    query = """
    SELECT contract_id,
           customer_name,
           contract_amount,
           invoice_amount,
           ROUND(
               CAST(invoice_amount AS REAL) -
               CAST(contract_amount AS REAL), 2
           ) AS difference
    FROM raw_billing_contracts
    WHERE ABS(
        CAST(invoice_amount AS REAL) -
        CAST(contract_amount AS REAL)
    ) > 0.005
    """

    for row in conn.execute(query):
        print(row)
