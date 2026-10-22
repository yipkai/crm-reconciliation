from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "output"


def generate_summary(results):
    """Calculate reconciliation quality metrics."""
    # Separate records requiring financial review
    financial_review = (
        results["duplicate_contract"]
        | results["invalid_amount"]
    )

    validated = results.loc[~financial_review]
    # Identify records that pass all reconciliation checks
    fully_reconciled = (
        (results["match_status"] == "Matched")
        & (~results["billing_discrepancy"])
        & (~results["duplicate_contract"])
        & (~results["invalid_amount"])
    )

    reconciled = results.loc[fully_reconciled]
    summary = {
        "total_billing_records": len(results),
        "matched_records": int(
            (results["match_status"] == "Matched").sum()
        ),
        "ambiguous_records": int(
            (results["match_status"] == "Ambiguous").sum()
        ),
        "unmatched_records": int(
            (results["match_status"] == "Unmatched").sum()
        ),
        "billing_discrepancies": int(
            results["billing_discrepancy"].sum()
        ),
        "invalid_amount_records": int(
            results["invalid_amount"].sum()
        ),
        "duplicate_contract_records": int(
            results["duplicate_contract"].sum()
        ),
        "total_invoice_amount": results["invoice_amount"].sum(),
        "total_contract_amount": results["contract_amount"].sum(),
        "net_billing_difference": results["difference"].sum(),
        "absolute_billing_difference": results["difference"].abs().sum(),
        "financial_review_records": int(financial_review.sum()),
        "eligible_financial_records": len(validated),
        "eligible_invoice_amount": validated["invoice_amount"].sum(),
        "eligible_contract_amount": validated["contract_amount"].sum(),
        "fully_reconciled_records": int(fully_reconciled.sum()),
        "fully_reconciled_invoice_amount": reconciled["invoice_amount"].sum(),
        "fully_reconciled_contract_amount": reconciled["contract_amount"].sum(),
    }

    return pd.DataFrame([summary])


def main():
    results = pd.read_csv(
        OUTPUT_DIR / "reconciliation_results.csv"
    )

    summary = generate_summary(results)

    output_file = OUTPUT_DIR / "summary_report.csv"

    summary.to_csv(output_file, index=False)

    print("\n--- DATA QUALITY SUMMARY ---")

    for column, value in summary.iloc[0].items():
        print(f"{column}: {value}")

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
