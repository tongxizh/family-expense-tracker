from __future__ import annotations

import pandas as pd


def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return monthly totals split by income and expense."""
    if df.empty:
        return pd.DataFrame(columns=["month", "income", "expenses", "net"])

    monthly = df.copy()
    monthly["month"] = monthly["transaction_date"].dt.to_period("M").astype(str)

    grouped = (
        monthly.groupby("month", as_index=False)
        .agg(
            income=("amount", lambda s: s[s > 0].sum()),
            expenses=("amount", lambda s: s[s < 0].sum()),
        )
        .sort_values("month")
    )
    grouped["net"] = grouped["income"] + grouped["expenses"]
    return grouped


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Return category-level totals for current dataset."""
    if df.empty:
        return pd.DataFrame(columns=["category", "total"])

    return (
        df.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=True)
        .rename(columns={"amount": "total"})
    )
