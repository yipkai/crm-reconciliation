# CRM and Billing Data Reconciliation

## Project Overview

A Python and SQL data-processing project designed to identify inconsistencies between customer relationship management (CRM) records and billing data.

The project demonstrates how businesses can improve data quality, identify duplicate customer records, investigate billing discrepancies, and produce reconciliation reports.

The system uses a sample dataset containing deliberately introduced data-quality problems.

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

## Sample Reconciliation Results

| Metric | Result |
|---|---:|
| Billing records processed | 22 |
| Successfully matched records | 19 |
| Ambiguous customer matches | 2 |
| Unmatched customer records | 1 |
| Billing discrepancies | 3 |
| Invalid financial amounts | 0 |
| Records with duplicate contract IDs | 2 |
| Records requiring financial review | 2 |
| Records eligible for preliminary financial totals | 20 |
| Total invoice amount | $59,300 |
| Total contract amount | $58,650 |
| Net billing difference | +$650 |
| Absolute billing difference | $850 |

The sample dataset contains a duplicate contract ID. Financial totals are therefore preliminary and should not be treated as audited or finalized figures.

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
