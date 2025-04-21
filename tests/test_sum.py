import pytest 
from expense_manager import add_expense, sum_expenses, expenses
from expense import Expense

@pytest.fixture()
def test_sum():
    expenses.clear()

def test_total():
    add_expense(Expense(10.0, "2025-04-20", "movie ticket"))
    add_expense(Expense(17.0, "2025-04-20", "food"))
    add_expense(Expense(125.0, "2025-04-20", "clothes"))
    
    total = sum_expenses()
    assert total == 152.0