import pytest
from expense import Expense
from expense_manager import add_expense, view_expenses, delete_expense, expenses

@pytest.fixture(autouse=True)
def clear_expense_list():
    expenses.clear()

def test_add_valid_expense():
    e = Expense(20.5, "2025-04-14", "Groceries", "Fruits and snacks")
    add_expense(e)
    assert len(view_expenses()) == 1
    assert view_expenses()[0].amount == 20.5
    assert view_expenses()[0].category == "Groceries"

def test_add_invalid_type():
    with pytest.raises(TypeError):
        add_expense("Not an Expense Object")

def test_view_expenses_empty():
    assert view_expenses() == []

def test_delete_expense_valid():
    e = Expense(10.0, "2025-04-13", "Transport", "Uber ride")
    add_expense(e)
    assert delete_expense(0) is True
    assert len(view_expenses()) == 0

def test_delete_expense_invalid():
    assert delete_expense(5) is False
