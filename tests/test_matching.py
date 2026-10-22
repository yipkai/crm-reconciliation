import pandas as pd

from src.matching import match_customer, normalize


def test_ambiguous_customer_match():
    crm = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "email": "billing@acme.com",
                "customer_name": "Acme Manufacturing",
            },
            {
                "customer_id": "C021",
                "email": "billing@acme.com",
                "customer_name": "Acme Mfg.",
            },
        ]
    )

    crm["match_email"] = crm["email"].apply(normalize)
    crm["match_name"] = crm["customer_name"].apply(normalize)

    bill = {
        "customer_email": "billing@acme.com",
        "customer_name": "Acme Manufacturing",
    }

    result = match_customer(bill, crm)

    assert result["match_status"] == "Ambiguous"
    assert result["match_count"] == 2
    assert result["customer_id"] == ""


def test_unmatched_customer():
    crm = pd.DataFrame(
        [
            {
                "customer_id": "C001",
                "email": "billing@acme.com",
                "customer_name": "Acme Manufacturing",
            }
        ]
    )

    crm["match_email"] = crm["email"].apply(normalize)
    crm["match_name"] = crm["customer_name"].apply(normalize)

    bill = {
        "customer_email": "unknown@example.com",
        "customer_name": "Unknown Company",
    }

    result = match_customer(bill, crm)

    assert result["match_status"] == "Unmatched"
    assert result["match_count"] == 0
