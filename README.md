# CRM and Billing Data Reconciliation

## Project Overview

A Python and SQL data-processing project designed to identify inconsistencies between customer relationship management (CRM) records and billing data.

The project demonstrates how businesses can improve data quality, identify duplicate customer records, investigate billing discrepancies, and produce reconciliation reports.

The system uses a sample dataset containing deliberately introduced data-quality problems.
## Reconciliation Results at a Glance

The system processed 22 sample billing records and identified several data-quality and financial reconciliation issues.

| Metric | Result |
|---|---:|
| Billing records processed | 22 |
| Fully reconciled records | **14 (63.6%)** |
| Records requiring investigation | **8 (36.4%)** |
| Ambiguous customer matches | 2 |
| Unmatched customer records | 1 |
| Billing discrepancies | 3 |
| Records with duplicate contract IDs | 2 |
| Net billing difference | +$650 |
| Absolute billing difference | $850 |
| Fully reconciled invoice value | **$40,500** |

## Example Reconciliation Exceptions

The reconciliation process generates an exception report identifying records that require further investigation.

The following examples come from the synthetic sample dataset.

| Contract ID | Customer | Issue | Financial Difference |
|---|---|---|---:|
| CTR001 | Acme Manufacturing | Ambiguous customer match | $0 |
| CTR003 | Canyon Office Supply | Billing discrepancy | +$250 |
| CTR005 | Evergreen Property Group | Ambiguous customer match | $0 |
| CTR006 | Frontier Logistics | Duplicate contract ID (2 records) | $0 |
| CTR008 | Highland Medical Supply | Billing discrepancy | -$100 |
| CTR015 | Oak Ridge Consulting | Billing discrepancy | +$500 |
| CTR021 | Summit Ridge Holdings | Unmatched customer | $0 |

### Understanding the Exceptions

**1. Ambiguous Customer Matches**

Acme Manufacturing and Evergreen Property Group each have multiple potential CRM matches.

The system flags these records rather than arbitrarily selecting a customer.

**2. Billing Discrepancies**

Three contracts contain differences between their contracted and invoiced amounts:

- Canyon Office Supply: Invoiced $250 above the contract amount.
- Highland Medical Supply: Invoiced $100 below the contract amount.
- Oak Ridge Consulting: Invoiced $500 above the contract amount.

The net billing difference is +$650, while the total absolute discrepancy is $850.

**3. Duplicate Contract Records**

Frontier Logistics appears twice under contract ID CTR006.

Both records are flagged for investigation and excluded from preliminary eligible financial totals.

The system preserves the original records rather than automatically deleting one.

**4. Unmatched Customer**

Summit Ridge Holdings has a billing record without a corresponding CRM customer match.

The record is flagged for investigation.

### Exception Reporting Approach

The system produces two complementary outputs:

- **Detailed exception report:** Identifies individual records requiring investigation.
- **Summary report:** Quantifies reconciliation results, financial discrepancies, and records passing automated checks.

This allows users to move from identifying a data-quality problem to investigating the specific records responsible.

*The exception report contains eight rows representing seven distinct contract IDs because CTR006 appears twice.*
### Key Findings

**Customer matching:** The reconciliation process identified two billing records with ambiguous customer matches and one record without a corresponding CRM customer.

**Financial discrepancies:** Three billing records contained invoice amounts that differed from their contract amounts. These discrepancies totaled $850 in absolute value, with a net difference of +$650.

**Duplicate contract detection:** Two billing records shared a contract identifier and were flagged for financial review rather than automatically removed.

**Reconciliation completeness:** Fourteen of the 22 billing records passed all implemented matching, duplicate-contract, financial-validation, and billing-discrepancy checks.

### Business Value

This workflow demonstrates how Python and SQL can help businesses:

- Identify inaccurate or inconsistent customer records.
- Detect billing discrepancies before relying on financial reports.
- Separate records requiring investigation from records that pass automated checks.
- Reduce manual reconciliation work through repeatable processing.
- Produce detailed exception reports and management-level summaries.

*All results are based on synthetic sample data. The figures demonstrate automated reconciliation controls and are not audited financial statements.*
## Business Problem

Businesses frequently maintain customer and financial information in separate systems.

Over time, these systems can develop inconsistencies, including:

- Duplicate customer records
- Missing or invalid email addresses
- Inconsistent customer names and phone numbers
- Unmatched customer accounts
- Incorrect invoice amounts
- Duplicate contract identifiers

These problems can lead to inaccurate reporting, inefficient operations, and financial discrepancies.

## Project Objectives

1. Import CRM and billing data into a SQLite database.
2. Clean and standardize customer information.
3. Identify potential duplicate customer records.
4. Match billing records against CRM customer records.
5. Detect billing discrepancies and invalid financial amounts.
6. Flag duplicate contracts for financial review.
7. Generate reconciliation and data-quality reports.
8. Validate processing logic through automated tests.

## Technologies Used

- Python
- pandas
- SQLite
- SQL
- pytest

## Processing Workflow

### 1. Data Generation

Generate sample CRM and billing datasets containing intentional inconsistencies.

### 2. Data Import

Import the CSV files into SQLite tables for structured storage and analysis.

### 3. Data Cleaning

Standardize customer names, email addresses, and phone numbers.

Identify missing and invalid email addresses.

### 4. Duplicate Detection

Identify potential duplicate customer records using normalized customer information.

### 5. Customer Reconciliation

Match billing records to CRM customers using normalized email addresses and customer names.

Classify results as:

- **Matched:** Exactly one customer record identified.
- **Ambiguous:** Multiple potential customer records identified.
- **Unmatched:** No corresponding customer record found.

### 6. Financial Validation

Compare invoice amounts with contract amounts.

Flag billing discrepancies and missing or invalid financial values.

Identify duplicate contract IDs requiring investigation.

### 7. Reporting

Generate detailed reconciliation results, exception reports, and summary metrics.

Separate records requiring financial review from records eligible for preliminary financial reporting.

### 8. Automated Testing

Use pytest to verify data cleaning, customer matching, financial validation, reconciliation behavior, and summary calculations.

## Output Files

The project generates the following reports:

| File | Description |
|---|---|
| `cleaned_customers.csv` | Standardized CRM customer records |
| `possible_duplicates.csv` | Potential duplicate customer records |
| `reconciliation_results.csv` | Complete billing reconciliation results |
| `reconciliation_exceptions.csv` | Records requiring investigation |
| `summary_report.csv` | Data-quality and financial summary |

Reports are saved in the `output/` directory.

## Running the Project

Install the required Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Generate sample data:

```bash
python -m src.generate_data
```

Import the data into SQLite:

```bash
python -m src.load_data
```

Clean customer records:

```bash
python -m src.clean_data
```

Identify potential duplicates:

```bash
python -m src.find_duplicates
```

Run the reconciliation:

```bash
python -m src.reconcile_data
```

Generate the summary report:

```bash
python -m src.summary_report
```

Run automated tests:

```bash
python -m pytest -v
```

## Testing

The project includes 11 automated tests covering:

- Customer data cleaning
- Duplicate customer matching
- Unmatched customer detection
- Financial amount validation
- SQL reconciliation behavior
- End-to-end reconciliation
- Summary report calculations
- Duplicate-contract financial controls

## Financial Reporting Controls

The system preserves original billing records rather than automatically deleting potential duplicates.

Records containing duplicate contract identifiers or invalid financial amounts are excluded from preliminary eligible financial totals and flagged for investigation.

This approach helps prevent unsupported assumptions from affecting financial reporting.

## Potential Improvements

Future enhancements could include:

- More advanced customer-matching algorithms
- Configurable matching rules
- Currency-format normalization
- Automated Excel reporting
- Interactive data-quality dashboards
- Processing larger datasets
- Integration with CRM and accounting platforms

## Project Purpose

This project demonstrates practical skills in Python automation, SQL, data cleaning, financial reconciliation, exception reporting, and automated testing.

It is intended as a portfolio example of a repeatable workflow for identifying and investigating business data-quality problems.
