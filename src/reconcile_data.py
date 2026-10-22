import sqlite3
from pathlib import Path

import pandas as pd

from src.matching import match_customer, normalize
from src.validation import validate_amounts


PROJECT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_DIR / "crm_reconciliation.db"
OUTPUT_DIR = PROJECT_DIR / "output"


def main(db_path=DB_PATH, output_dir=OUTPUT_DIR):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # STEP 1: Load the original records from SQLite

    with sqlite3.connect(db_path) as conn:

        crm = pd.read_sql_query(
            "SELECT * FROM raw_crm_customers",
            conn
        )

        billing = pd.read_sql_query(
            "SELECT * FROM raw_billing_contracts",
            conn
        )


    print(f"CRM records: {len(crm)}")
    print(f"Billing records: {len(billing)}")


    # STEP 2: Normalize matching fields

    crm["match_email"] = crm["email"].apply(normalize)
    crm["match_name"] = crm["customer_name"].apply(normalize)

    billing["match_email"] = billing["customer_email"].apply(normalize)
    billing["match_name"] = billing["customer_name"].apply(normalize)


    # STEP 3: Match billing records to CRM customers

    results = []

    for _, bill in billing.iterrows():

        # Use our tested matching function
        match = match_customer(bill, crm)

        results.append({
            "contract_id": bill["contract_id"],
            "billing_customer": bill["customer_name"],
            "customer_id": match["customer_id"],
            "match_method": match["match_method"],
            "match_status": match["match_status"],
            "match_count": match["match_count"],
            "contract_amount": bill["contract_amount"],
            "invoice_amount": bill["invoice_amount"],
        })


    # STEP 4: Create reconciliation DataFrame

    df = pd.DataFrame(results)

    df["contract_amount"] = pd.to_numeric(
        df["contract_amount"],
        errors="coerce"
    )

    df["invoice_amount"] = pd.to_numeric(
        df["invoice_amount"],
        errors="coerce"
    )

    # Identify missing or invalid financial amounts
    df = validate_amounts(df)

    df["difference"] = (
        df["invoice_amount"] - df["contract_amount"]
    ).round(2)


    # STEP 5: Identify exceptions

    df["billing_discrepancy"] = df["difference"].abs() > 0.005

    # Identify repeated contract IDs
    df["duplicate_contract"] = df.duplicated(
        subset=["contract_id"],
        keep=False
    )

    exceptions = df[
        (df["match_status"] != "Matched")
        | (df["billing_discrepancy"])
        | (df["duplicate_contract"])
        | (df["invalid_amount"])
    ].copy()


    # STEP 6: Save reports

    df.to_csv(
        output_dir / "reconciliation_results.csv",
        index=False
    )

    exceptions.to_csv(
        output_dir / "reconciliation_exceptions.csv",
        index=False
    )


    # STEP 7: Print summary

    print("\n--- RECONCILIATION SUMMARY ---")

    print(f"Billing records processed: {len(df)}")

    print(
        f"Matched: "
        f"{(df['match_status'] == 'Matched').sum()}"
    )

    print(
        f"Ambiguous: "
        f"{(df['match_status'] == 'Ambiguous').sum()}"
    )

    print(
        f"Unmatched: "
        f"{(df['match_status'] == 'Unmatched').sum()}"
    )

    print(
        f"Billing discrepancies: "
        f"{df['billing_discrepancy'].sum()}"
    )

    print(
        f"Records with duplicate contract IDs: "
        f"{df['duplicate_contract'].sum()}"
    )

    print(f"Exception records: {len(exceptions)}")

    print("\nReports saved to output directory.")

    print(f"Invalid financial amounts: {df['invalid_amount'].sum()}")

if __name__ == "__main__":
    main()
