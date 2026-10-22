import pandas as pd

from src.validation import validate_amounts


def test_invalid_invoice_amount():
    data = pd.DataFrame(
        [
            {
                "contract_amount": "1200.00",
                "invoice_amount": "ABC",
            },
            {
                "contract_amount": "1500.00",
                "invoice_amount": "1500.00",
            },
        ]
    )

    result = validate_amounts(data)

    assert result["invalid_amount"].sum() == 1
    assert pd.isna(result.loc[0, "invoice_amount"])
    assert result.loc[1, "invoice_amount"] == 1500.00


def test_missing_contract_amount():
    data = pd.DataFrame(
        [
            {
                "contract_amount": "",
                "invoice_amount": "1000.00",
            }
        ]
    )

    result = validate_amounts(data)

    assert result["invalid_amount"].sum() == 1
