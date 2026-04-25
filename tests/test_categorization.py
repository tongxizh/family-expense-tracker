from family_expense_tracker.categorization import categorize, infer_merchant


def test_categorize_income_rule():
    assert categorize("ACME Payroll Direct Deposit") == "Income"


def test_categorize_default():
    assert categorize("Unknown Vendor Charge") == "Uncategorized"


def test_infer_merchant_returns_trimmed_value():
    assert infer_merchant("Coffee House - Downtown") == "Coffee House"
