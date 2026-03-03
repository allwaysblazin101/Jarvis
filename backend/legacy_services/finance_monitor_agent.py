def analyze_financial_risk(bank_transactions):

    total_spend = sum(
        t["amount"]
        for t in bank_transactions
        if t["amount"] > 0
    )

    if total_spend > 2000:
        return "High spending month"

    return "Spending normal"
EOF