class Expense:
    def __init__(self, amount, date, category, description=""):
        self.amount = float(amount)
        self.date = date  # Expecting format: "YYYY-MM-DD"
        self.category = category
        self.description = description

    def __str__(self):
        return f"{self.date} | {self.category} | ${self.amount:.2f} | {self.description}"
