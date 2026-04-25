# Family Expense Tracker (Local-First MVP)

A local-first Python app for tracking family income and expenses from bank and credit card statements.

## Features

- Streamlit local dashboard UI.
- SQLite + SQLAlchemy storage on your machine.
- CSV and Excel statement upload support.
- Canonical transaction schema:
  - `transaction_date`
  - `description`
  - `amount`
  - `merchant`
  - `category`
  - `source_file`
- Simple rule-based categorization.
- Monthly summary and category charts.
- Included anonymized sample data.
- Pytest test suite.

## Project Structure

- `app.py` - Streamlit app entrypoint.
- `family_expense_tracker/` - core package.
- `sample_data/` - anonymized statement examples.
- `tests/` - automated tests.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Usage

1. Start the app:

```bash
streamlit run app.py
```

2. Upload one or more CSV/XLSX statements.
3. Review monthly summaries, category breakdown, and transactions.

You can test import logic with the included sample file:

- `sample_data/sample_statement.csv`

## Privacy Notes

- This MVP is local-first: data is written to a local SQLite file (`family_expense_tracker.sqlite`) by default.
- No cloud sync, external API, or remote database is included.
- `.gitignore` prevents common accidental commits of raw financial files and local databases.
- Use only anonymized or scrubbed sample files when sharing this repository.

## Testing

```bash
pytest
```

## Roadmap

- Add account-level views and running balances.
- Add duplicate detection across statement uploads.
- Improve categorization with configurable household rules.
- Add recurring transaction detection and budgeting targets.
- Add export options for monthly reports.
