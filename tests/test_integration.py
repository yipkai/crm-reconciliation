import sqlite3

import pandas as pd

from src.reconcile_data import main


def test_complete_reconciliation(tmp_path):
    # Create a temporary database and output directory
    db_path = tmp_path / "test_reconciliation.db"
    output_dir = tmp_path / "output"

    # Create sample CRM records
    crm = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "customer_name": "Acme Manufacturing",
                "email": "billing@acme.com",
                "phone": "602-555-0101",
            },
            {
                "customer_id": "C002",
                "customer_name": "Acme Mfg.",
                "email": "billing@acme.com",
                "phone": "602-555-0101",
            },
            {
                "customer_id": "C003",
                "customer_name": "Blue Sky Consulting",
                "email": "accounts@bluesky.com",
                "phone": "602-555-0102",
            },
        ]
    )

    # Create sample billing records
    billing = pd.DataFrame(
        [
            {
                "contract_id": "CTR001",
                "customer_name": "Acme Manufacturing",
                "customer_email": "billing@acme.com",
                "contract_amount": "1200.00",
                "invoice_amount": "1200.00",
            },
            {
                "contract_id": "CTR002",
                "customer_name": "Blue Sky Consulting",
                "customer_email": "accounts@bluesky.com",
                "contract_amount": "1500.00",
                "invoice_amount": "1750.00",
            },
            {
                "contract_id": "CTR003",
                "customer_name": "Unknown Company",
                "customer_email": "unknown@example.com",
                "contract_amount": "900.00",
                "invoice_amount": "900.00",
            },
        ]
    )

    # Load sample data into temporary SQLite tables
    with sqlite3.connect(db_path) as conn:
        crm.to_sql(
            "raw_crm_customers",
            conn,
            index=False,
        )

        billing.to_sql(
            "raw_billing_contracts",
            conn,
            index=False,
        )

    # Execute the actual reconciliation program
    main(db_path=db_path, output_dir=output_dir)

    # Read the generated reports
    results = pd.read_csv(
        output_dir / "reconciliation_results.csv"
    )

    exceptions = pd.read_csv(
        output_dir / "reconciliation_exceptions.csv"
    )

    # Every original billing record must appear once
    assert len(results) == 3

    # Check matching results
    assert (
        results["match_status"].value_counts().to_dict()
        == {"Ambiguous": 1, "Matched": 1, "Unmatched": 1}
    )

    # Verify Acme was identified as ambiguous
    acme = results.loc[
        results["contract_id"] == "CTR001"
    ].iloc[0]

    assert acme["match_status"] == "Ambiguous"
    assert acme["match_count"] == 2

    # Verify billing discrepancy
    blue_sky = results.loc[
        results["contract_id"] == "CTR002"
    ].iloc[0]

    assert blue_sky["difference"] == 250.00
    assert bool(blue_sky["billing_discrepancy"])

    # Verify that the JOIN did not inflate invoice totals
    assert results["invoice_amount"].sum() == 3850.00

    # Verify all three records require investigation
    assert len(exceptions) == 3
