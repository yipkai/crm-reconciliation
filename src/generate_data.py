
import csv
import random
from pathlib import Path

# Always write files to the project's data directory,
# regardless of the directory from which the script is run.
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR  data
DATA_DIR.mkdir(exist_ok=True)

random.seed(42)

# Base customer records
customers = [
    (C001, Acme Manufacturing, billing@acme.com, 602-555-0101),
    (C002, Blue Sky Consulting, accounts@bluesky.com, 602-555-0102),
    (C003, Canyon Office Supply, info@canyon.com, 602-555-0103),
    (C004, Desert Peak Services, admin@desertpeak.com, 602-555-0104),
    (C005, Evergreen Property Group, finance@evergreen.com, 602-555-0105),
    (C006, Frontier Logistics, billing@frontier.com, 602-555-0106),
    (C007, Golden Gate Industries, accounts@goldengate.com, 602-555-0107),
    (C008, Highland Medical Supply, office@highland.com, 602-555-0108),
    (C009, Ironwood Technologies, payables@ironwood.com, 602-555-0109),
    (C010, Juniper Creative Studio, hello@juniper.com, 602-555-0110),
    (C011, Keystone Building Group, billing@keystone.com, 602-555-0111),
    (C012, Lighthouse Marketing, accounts@lighthouse.com, 602-555-0112),
    (C013, Mesa Valley Foods, finance@mesavalley.com, 602-555-0113),
    (C014, Northstar Equipment, billing@northstar.com, 602-555-0114),
    (C015, Oak Ridge Consulting, office@oakridge.com, 602-555-0115),
    (C016, Pioneer Distribution, accounts@pioneer.com, 602-555-0116),
    (C017, Quartz Mountain LLC, admin@quartz.com, 602-555-0117),
    (C018, Red Rock Contractors, billing@redrock.com, 602-555-0118),
    (C019, Silverline Printing, info@silverline.com, 602-555-0119),
    (C020, Timber Creek Services, finance@timbercreek.com, 602-555-0120),
]

# Create CRM data and deliberately introduce data-quality problems.
crm_rows = []

for i, (customer_id, name, email, phone) in enumerate(customers)
    row = {
        customer_id customer_id,
        customer_name name,
        email email,
        phone phone,
    }

    if i == 1
        row[customer_name] =   BLUE SKY CONSULTING
        row[email] = ACCOUNTS@BLUESKY.COM
        row[phone] = (602) 555-0102

    elif i == 3
        row[customer_name] = Desert Peak  Services

    elif i == 4
        row[email] =

    elif i == 6
        row[email] = not-an-email

    elif i == 8
        row[phone] =

    elif i == 10
        row[customer_name] = KEYSTONE BUILDING GROUP

    elif i == 12
        row[phone] = 602.555.0113

    elif i == 16
        row[customer_name] =  Quartz Mountain LLC

    crm_rows.append(row)

# Add an exact duplicate record.
crm_rows.append(crm_rows[4].copy())

# Add a likely duplicate customer with a different ID.
crm_rows.append({
    customer_id C021,
    customer_name Acme Mfg.,
    email billing@acme.com,
    phone 6025550101,
})

# Add a record with several missing fields.
crm_rows.append({
    customer_id C022,
    customer_name Valley View Enterprises,
    email ,
    phone ,
})


# Generate billing records.
billing_rows = []

for i, (customer_id, name, email, phone) in enumerate(customers)
    contract_amount = 1200 + (i  150)
    invoice_amount = contract_amount

    # Three deliberate billing discrepancies.
    if i == 2
        invoice_amount = contract_amount + 250
    elif i == 7
        invoice_amount = contract_amount - 100
    elif i == 14
        invoice_amount = contract_amount + 500

    billing_name = name
    billing_email = email

    # Introduce formatting inconsistencies.
    if i == 1
        billing_name = Blue Sky Consulting
        billing_email = email.upper()
    elif i == 5
        billing_name = FRONTIER LOGISTICS
    elif i == 9
        billing_name = Juniper Creative Studio
        billing_email =
    elif i == 13
        billing_name = North Star Equipment
    elif i == 16
        billing_name = Quartz Mountain, LLC

    billing_rows.append({
        contract_id fCTR{i + 103d},
        customer_name billing_name,
        customer_email billing_email,
        contract_amount f{contract_amount.2f},
        invoice_amount f{invoice_amount.2f},
    })

# Duplicate a billing record.
billing_rows.append(billing_rows[5].copy())

# Add a billing customer with no corresponding CRM record.
billing_rows.append({
    contract_id CTR021,
    customer_name Summit Ridge Holdings,
    customer_email billing@summitridge.com,
    contract_amount 4200.00,
    invoice_amount 4200.00,
})


def write_csv(filename, rows)
    Write a list of dictionaries to a CSV file.
    filepath = DATA_DIR  filename

    with filepath.open(w, newline=, encoding=utf-8) as file
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(fCreated {filepath.relative_to(PROJECT_DIR)} ({len(rows)} rows))


if __name__ == __main__
    write_csv(crm_customers.csv, crm_rows)
    write_csv(billing_contracts.csv, billing_rows)

    print(nSample data generation complete.)
