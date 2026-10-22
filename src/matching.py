import pandas as pd


def normalize(value):
    """Standardize text for matching."""
    if pd.isna(value):
        return ""

    return " ".join(str(value).lower().split())


def match_customer(bill, crm):
    """Find CRM customers matching a billing record."""

    billing_email = normalize(bill["customer_email"])
    billing_name = normalize(bill["customer_name"])

    # First attempt: email match
    email_matches = crm[
        (crm["match_email"] == billing_email)
        & (crm["match_email"] != "")
    ]

    if len(email_matches) > 0:
        matches = email_matches
        match_method = "Email"

    else:
        # Second attempt: company-name match
        matches = crm[
            (crm["match_name"] == billing_name)
            & (crm["match_name"] != "")
        ]

        match_method = "Name"

    if len(matches) == 0:
        return {
            "customer_id": "",
            "match_status": "Unmatched",
            "match_method": match_method,
            "match_count": 0,
        }

    if len(matches) > 1:
        return {
            "customer_id": "",
            "match_status": "Ambiguous",
            "match_method": match_method,
            "match_count": len(matches),
        }

    return {
        "customer_id": matches.iloc[0]["customer_id"],
        "match_status": "Matched",
        "match_method": match_method,
        "match_count": 1,
    }
