import pandas as pd

from src.summary_report import generate_summary


def test_summary_report():
    data = pd.DataFrame(
        [
            {
                "match_status": "Matched",
                "billing_discrepancy": False,
                "invalid_amount": False,
                "duplicate_contract": False,
                "invoice_amount": 1000.00,
                "contract_amount": 1000.00,
                "difference": 0.00,
            },
            {
                "match_status": "Matched",
                "billing_discrepancy": True,
                "invalid_amount": False,
                "duplicate_contract": False,
                "invoice_amount": 1250.00,
                "contract_amount": 1000.00,
                "difference": 250.00,
            },
            {
                "match_status": "Unmatched",
                "billing_discrepancy": True,
                "invalid_amount": False,
                "duplicate_contract": False,
                "invoice_amount": 900.00,
                "contract_amount": 1000.00,
                "difference": -100.00,
            },
        ]
    )

    summary = generate_summary(data).iloc[0]

    assert summary["total_billing_records"] == 3
    assert summary["matched_records"] == 2
    assert summary["unmatched_records"] == 1
    assert summary["billing_discrepancies"] == 2

    assert summary["total_invoice_amount"] == 3150.00
    assert summary["total_contract_amount"] == 3000.00

    assert summary["net_billing_difference"] == 150.00
    assert summary["absolute_billing_difference"] == 350.00

def test_duplicate_contract_excluded_from_eligible_totals():
    data = pd.DataFrame(
        [
            {
                "match_status": "Matched",
                "billing_discrepancy": False,
                "invalid_amount": False,
                "duplicate_contract": False,
                "invoice_amount": 1000.00,
                "contract_amount": 1000.00,
                "difference": 0.00,
            },
            {
                "match_status": "Matched",
                "billing_discrepancy": False,
                "invalid_amount": False,
                "duplicate_contract": True,
                "invoice_amount": 2000.00,
                "contract_amount": 2000.00,
                "difference": 0.00,
            },
        ]
    )

    summary = generate_summary(data).iloc[0]

    assert summary["total_billing_records"] == 2
    assert summary["financial_review_records"] == 1
    assert summary["eligible_financial_records"] == 1

    assert summary["total_invoice_amount"] == 3000.00
    assert summary["eligible_invoice_amount"] == 1000.00
    assert summary["eligible_contract_amount"] == 1000.00
