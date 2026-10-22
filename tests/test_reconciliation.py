import sqlite3

import pandas as pd


def test_duplicate_customer_join():
    # Create an in-memory SQLite database
    with sqlite3.connect(":memory:") as conn:

        # Create sample billing data
        billing = pd.DataFrame([
            {
                "contract_id": "CTR001",
                "customer_email": "billing@acme.com",
                "invoice_amount": 1200.00,
            }
        ])

        # Create two CRM records with the same email
        crm = pd.DataFrame([
            {
                "customer_id": "C001",
                "email": "billing@acme.com",
            },
            {
                "customer_id": "C021",
                "email": "billing@acme.com",
            },
        ])

        billing.to_sql("billing", conn, index=False)
        crm.to_sql("crm", conn, index=False)

        # Count CRM matches without duplicating billing rows
        query = """
        SELECT
            b.contract_id,
            b.invoice_amount,
            (
                SELECT COUNT(*)
                FROM crm c
                WHERE c.email = b.customer_email
            ) AS match_count
        FROM billing b
        """

        result = pd.read_sql_query(query, conn)

    # Verify that the billing record appears only once
    assert len(result) == 1

    # Verify that two CRM customers match
    assert result.iloc[0]["match_count"] == 2

    # Verify that the invoice amount is not doubled
    assert result["invoice_amount"].sum() == 1200.00
