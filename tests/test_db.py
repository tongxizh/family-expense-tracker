from pathlib import Path

from family_expense_tracker.db import fetch_all_transactions, initialize_database, save_transactions


def test_save_and_fetch_transactions(tmp_path: Path):
    db_path = tmp_path / "test.sqlite"
    initialize_database(db_path)

    count = save_transactions(
        [
            {
                "transaction_date": __import__("datetime").date(2026, 1, 1),
                "description": "Salary Payroll",
                "amount": 3000.0,
                "merchant": "ACME",
                "category": "Income",
                "source_file": "sample.csv",
            }
        ],
        db_path,
    )

    assert count == 1
    records = fetch_all_transactions(db_path)
    assert len(records) == 1
    assert records[0].category == "Income"
