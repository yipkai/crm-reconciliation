import pandas as pd


def validate_amounts(df):
    """Convert financial amounts and flag invalid values."""

    df = df.copy()

    df["contract_amount"] = pd.to_numeric(
        df["contract_amount"],
        errors="coerce",
    )

    df["invoice_amount"] = pd.to_numeric(
        df["invoice_amount"],
        errors="coerce",
    )

    df["invalid_amount"] = (
        df["contract_amount"].isna()
        | df["invoice_amount"].isna()
    )

    return df
