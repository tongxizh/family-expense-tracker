from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from family_expense_tracker.categorization import categorize, infer_merchant

DATE_CANDIDATES = ["date", "transaction_date", "posted date", "posting date"]
DESCRIPTION_CANDIDATES = ["description", "details", "memo", "narrative"]
AMOUNT_CANDIDATES = ["amount", "transaction amount", "debit", "credit"]


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip().lower() for col in df.columns]
    return df


def _pick_column(columns: list[str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        for col in columns:
            if candidate == col:
                return col
    return None


def _load_dataframe(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported file format: {suffix}")


def parse_statement(path: Path) -> list[dict]:
    """Parse CSV/Excel statement into canonical transaction schema."""
    df = _normalize_columns(_load_dataframe(path))

    date_col = _pick_column(df.columns.tolist(), DATE_CANDIDATES)
    description_col = _pick_column(df.columns.tolist(), DESCRIPTION_CANDIDATES)
    amount_col = _pick_column(df.columns.tolist(), AMOUNT_CANDIDATES)

    if not (date_col and description_col and amount_col):
        raise ValueError(
            "Statement must include date, description, and amount-like columns."
        )

    normalized_rows: list[dict] = []
    for _, row in df.iterrows():
        if pd.isna(row[date_col]) or pd.isna(row[description_col]) or pd.isna(row[amount_col]):
            continue

        transaction_date = pd.to_datetime(row[date_col]).date()
        description = str(row[description_col]).strip()
        amount = float(row[amount_col])

        normalized_rows.append(
            {
                "transaction_date": transaction_date,
                "description": description,
                "amount": amount,
                "merchant": infer_merchant(description),
                "category": categorize(description),
                "source_file": path.name,
            }
        )

    return normalized_rows


def dataframe_from_transactions(rows: list[dict]) -> pd.DataFrame:
    """Convert parsed rows to DataFrame for dashboard usage."""
    if not rows:
        return pd.DataFrame(
            columns=[
                "transaction_date",
                "description",
                "amount",
                "merchant",
                "category",
                "source_file",
            ]
        )

    df = pd.DataFrame(rows)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df
