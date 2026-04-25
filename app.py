from pathlib import Path

import pandas as pd
import streamlit as st

from family_expense_tracker.db import (
    DEFAULT_DB_PATH,
    fetch_all_transactions,
    initialize_database,
    save_transactions,
)
from family_expense_tracker.parser import parse_statement
from family_expense_tracker.summary import category_breakdown, monthly_summary

st.set_page_config(page_title="Family Expense Tracker", page_icon="💰", layout="wide")
st.title("💰 Family Expense Tracker (Local-First MVP)")
st.caption("All data remains on your local machine unless you choose to share files.")

initialize_database(DEFAULT_DB_PATH)

uploaded_files = st.file_uploader(
    "Upload CSV or Excel statements",
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True,
)

if uploaded_files:
    imported_total = 0
    with st.spinner("Parsing statements and saving transactions..."):
        for uploaded in uploaded_files:
            target = Path(uploaded.name)
            target.write_bytes(uploaded.getvalue())
            rows = parse_statement(target)
            imported_total += save_transactions(rows, DEFAULT_DB_PATH)
            target.unlink(missing_ok=True)
    st.success(f"Imported {imported_total} transactions.")

records = fetch_all_transactions(DEFAULT_DB_PATH)
if not records:
    st.info("No transactions yet. Upload a sample statement to begin.")
    st.stop()

transactions_df = pd.DataFrame(
    [
        {
            "transaction_date": t.transaction_date,
            "description": t.description,
            "amount": t.amount,
            "merchant": t.merchant,
            "category": t.category,
            "source_file": t.source_file,
        }
        for t in records
    ]
)
transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"])

st.subheader("Monthly Summary")
summary_df = monthly_summary(transactions_df)
st.dataframe(summary_df, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.metric("Total Income", f"${summary_df['income'].sum():,.2f}")
with col2:
    st.metric("Total Expenses", f"${summary_df['expenses'].sum():,.2f}")

st.subheader("Category Breakdown")
category_df = category_breakdown(transactions_df)
st.bar_chart(category_df.set_index("category")["total"])

st.subheader("Transactions")
st.dataframe(transactions_df.sort_values("transaction_date", ascending=False), use_container_width=True)
