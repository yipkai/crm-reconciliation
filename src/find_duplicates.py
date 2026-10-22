from pathlib import Path

import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "output"

# Load cleaned customer data
df = pd.read_csv(
    OUTPUT_DIR / "cleaned_customers.csv",
    dtype=str,
    keep_default_na=False
)

print(f"Total customer records: {len(df)}")


# Find customers sharing the same email address
email_duplicates = df[
    (df["email"] != "") &
    df.duplicated(subset=["email"], keep=False)
].copy()

print("\n--- CUSTOMERS SHARING EMAIL ADDRESSES ---")

print(
    email_duplicates.loc[
        :, ["customer_id", "customer_name", "email"]
    ].to_string(index=False)
)


# Find customers sharing the same phone number
phone_duplicates = df[
    (df["phone"] != "") &
    df.duplicated(subset=["phone"], keep=False)
].copy()

print("\n--- CUSTOMERS SHARING PHONE NUMBERS ---")

print(
    phone_duplicates.loc[
        :, ["customer_id", "customer_name", "phone"]
    ].to_string(index=False)
)


# Identify records sharing an email or phone number
possible_duplicates = df[
    df.index.isin(email_duplicates.index) |
    df.index.isin(phone_duplicates.index)
].copy()

# Save potential duplicates for review
output_file = OUTPUT_DIR / "possible_duplicates.csv"

possible_duplicates.to_csv(output_file, index=False)

print(f"\nPotential duplicate records: {len(possible_duplicates)}")
print(f"Report saved to: {output_file}")
