from datetime import date

from sqlalchemy import Date, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarative model."""


class Transaction(Base):
    """Canonical transaction schema for imported statement rows."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    merchant: Mapped[str] = mapped_column(String(255), nullable=False, default="Unknown")
    category: Mapped[str] = mapped_column(String(255), nullable=False, default="Uncategorized")
    source_file: Mapped[str] = mapped_column(String(255), nullable=False)
