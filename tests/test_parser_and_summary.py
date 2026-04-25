from pathlib import Path

import pandas as pd

from family_expense_tracker.parser import parse_statement
from family_expense_tracker.summary import monthly_summary


def test_parse_statement_csv(tmp_path: Path):
    statement = tmp_path / "statement.csv"
    statement.write_text(
        "transaction_date,description,amount\n"
        "2026-01-01,ACME Payroll,1000\n"
        "2026-01-02,Green Grocery,-42.5\n",
        encoding="utf-8",
    )

    rows = parse_statement(statement)

    assert len(rows) == 2
    assert rows[0]["category"] == "Income"
    assert rows[1]["category"] == "Groceries"
    assert rows[0]["source_file"] == "statement.csv"


def test_monthly_summary_groups_income_and_expense():
    df = pd.DataFrame(
        {
            "transaction_date": pd.to_datetime(["2026-01-01", "2026-01-05", "2026-02-01"]),
            "amount": [1000, -200, -100],
            "category": ["Income", "Housing", "Utilities"],
        }
    )

    summary = monthly_summary(df)

    january = summary.loc[summary["month"] == "2026-01"].iloc[0]
    assert january["income"] == 1000
    assert january["expenses"] == -200
    assert january["net"] == 800
