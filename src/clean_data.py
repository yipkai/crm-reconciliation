import re
from pathlib import Path

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_DIR = PROJECT_DIR / "output"


def clean_name(name):
    if not name:
        return ""

    return " ".join(name.split()).title()


def clean_email(email):
    if not email:
        return ""

    return email.strip().lower()


def clean_phone(phone):
    if not phone:
        return ""

    digits = re.sub(r"\D", "", phone)

    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"

    return phone.strip()


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(
        DATA_DIR / "crm_customers.csv",
        dtype=str,
        keep_default_na=False,
    )

    print(f"Original CRM records: {len(df)}")

    df["customer_name"] = df["customer_name"].apply(clean_name)
    df["email"] = df["email"].apply(clean_email)
    df["phone"] = df["phone"].apply(clean_phone)

    email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    df["email_valid"] = df["email"].str.fullmatch(email_pattern)

    df["is_duplicate"] = df.duplicated(
        subset=["customer_id", "customer_name", "email", "phone"],
        keep="first",
    )

    output_file = OUTPUT_DIR / "cleaned_customers.csv"

    df.to_csv(output_file, index=False)

    print(f"Cleaned CRM records: {len(df)}")
    print(f"Invalid or missing emails: {(~df['email_valid']).sum()}")
    print(f"Exact duplicate records: {df['is_duplicate'].sum()}")
    print(f"\nCleaned data saved to: {output_file}")


if __name__ == "__main__":
    main()
