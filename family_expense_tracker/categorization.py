from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    keyword: str
    category: str


RULES: tuple[Rule, ...] = (
    Rule("grocery", "Groceries"),
    Rule("supermarket", "Groceries"),
    Rule("rent", "Housing"),
    Rule("mortgage", "Housing"),
    Rule("uber", "Transport"),
    Rule("lyft", "Transport"),
    Rule("gas", "Transport"),
    Rule("fuel", "Transport"),
    Rule("netflix", "Entertainment"),
    Rule("spotify", "Entertainment"),
    Rule("restaurant", "Dining"),
    Rule("coffee", "Dining"),
    Rule("salary", "Income"),
    Rule("payroll", "Income"),
    Rule("bonus", "Income"),
    Rule("electric", "Utilities"),
    Rule("water", "Utilities"),
    Rule("internet", "Utilities"),
    Rule("pharmacy", "Healthcare"),
    Rule("clinic", "Healthcare"),
)


def categorize(description: str) -> str:
    """Assign a category from a basic keyword ruleset."""
    normalized = description.lower()
    for rule in RULES:
        if rule.keyword in normalized:
            return rule.category
    return "Uncategorized"


def infer_merchant(description: str) -> str:
    """Infer merchant from the first chunk of statement description."""
    clean = " ".join(description.replace("*", " ").split())
    merchant = clean.split("  ")[0].split("-")[0].strip()
    return merchant[:255] if merchant else "Unknown"
