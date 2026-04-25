from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from family_expense_tracker.models import Base, Transaction


DEFAULT_DB_PATH = Path("family_expense_tracker.sqlite")


def get_engine(db_path: Path = DEFAULT_DB_PATH):
    """Create an engine for the local sqlite database."""
    return create_engine(f"sqlite:///{db_path}", future=True)


def initialize_database(db_path: Path = DEFAULT_DB_PATH) -> None:
    """Initialize local database if it doesn't exist."""
    engine = get_engine(db_path)
    Base.metadata.create_all(engine)


def save_transactions(rows: list[dict], db_path: Path = DEFAULT_DB_PATH) -> int:
    """Persist normalized transactions and return count saved."""
    if not rows:
        return 0

    engine = get_engine(db_path)
    with Session(engine) as session:
        for row in rows:
            session.add(Transaction(**row))
        session.commit()
    return len(rows)


def fetch_all_transactions(db_path: Path = DEFAULT_DB_PATH) -> list[Transaction]:
    """Load all transactions sorted by date descending."""
    engine = get_engine(db_path)
    with Session(engine) as session:
        result = session.execute(
            select(Transaction).order_by(Transaction.transaction_date.desc())
        )
        return [record[0] for record in result.all()]
