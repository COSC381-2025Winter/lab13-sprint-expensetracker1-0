import pytest
from expense_manager import view_expenses, Expense
from datetime import date
import pandas as pd

# Sample expenses for testing
sample_expenses = [
    Expense(amount=10.0, date="2024-04-10", category="Food", description="Lunch"),
    Expense(amount=25.5, date="2024-04-15", category="Transport", description="Bus fare"),
    Expense(amount=50.0, date="2024-04-20", category="Entertainment", description="Movie"),
    Expense(amount=15.0, date="2024-04-20", category="Food", description="Snacks"),
    Expense(amount=100.0, date="2024-04-25", category="Bills", description="Internet"),
]

# Fixture to set up and tear down the global expenses list for each test
@pytest.fixture(autouse=True)
def manage_expenses(monkeypatch):
    """Sets the global expenses list for a test and clears it afterwards."""
    # Use monkeypatch to modify the global list within expense_manager
    monkeypatch.setattr('expense_manager.expenses', sample_expenses[:]) # Use a copy
    yield # Run the test
    # Teardown is implicitly handled by the next test's setup or can be explicit
    monkeypatch.setattr('expense_manager.expenses', [])

# --- Test Cases ---

def test_view_expenses_no_filter():
    """Test viewing expenses with no date filters."""
    result = view_expenses()
    assert len(result) == len(sample_expenses)
    assert result == sample_expenses # Order should be preserved

def test_view_expenses_start_date():
    """Test filtering with only a start date."""
    start = "2024-04-16"
    result = view_expenses(start_date=start)
    assert len(result) == 3
    assert all(exp.date >= start for exp in result)
    assert result[0].date == "2024-04-20"
    assert result[1].date == "2024-04-20"
    assert result[2].date == "2024-04-25"

def test_view_expenses_end_date():
    """Test filtering with only an end date."""
    end = "2024-04-19"
    result = view_expenses(end_date=end)
    assert len(result) == 2
    assert all(exp.date <= end for exp in result)
    assert result[0].date == "2024-04-10"
    assert result[1].date == "2024-04-15"

def test_view_expenses_date_range():
    """Test filtering with both start and end dates."""
    start = "2024-04-12"
    end = "2024-04-22"
    result = view_expenses(start_date=start, end_date=end)
    assert len(result) == 3
    assert all(start <= exp.date <= end for exp in result)
    assert result[0].date == "2024-04-15"
    assert result[1].date == "2024-04-20"
    assert result[2].date == "2024-04-20"

def test_view_expenses_exact_date():
    """Test filtering for a single exact date."""
    exact_date = "2024-04-20"
    result = view_expenses(start_date=exact_date, end_date=exact_date)
    assert len(result) == 2
    assert all(exp.date == exact_date for exp in result)
    assert result[0].category == "Entertainment"
    assert result[1].category == "Food"

def test_view_expenses_outside_range():
    """Test filtering with a range that excludes all sample expenses."""
    start = "2024-05-01"
    end = "2024-05-10"
    result = view_expenses(start_date=start, end_date=end)
    assert len(result) == 0

def test_view_expenses_empty_list(monkeypatch):
    """Test filtering when the global expenses list is empty."""
    monkeypatch.setattr('expense_manager.expenses', [])
    result_no_filter = view_expenses()
    result_with_filter = view_expenses(start_date="2024-01-01", end_date="2024-12-31")
    assert len(result_no_filter) == 0
    assert len(result_with_filter) == 0

# test_total_expense_summary and test_category_expense_summary developed using ChatGPT on 4/19/25
# Prompt: "create a test function similar to what we already have to test that summary of total expenses,
#          and summary by category works (previous code copy and pasted in prompt)"
def test_total_expense_summary():
    # Arrange
    """Test calculation of total expenses."""
    df = pd.DataFrame([{
        "Amount": exp.amount,
        "Category": exp.category,
        "Date": exp.date,
        "Description": exp.description
    } for exp in sample_expenses])
    
    # Act
    total = df["Amount"].sum()
    expected_total = sum(exp.amount for exp in sample_expenses)
    
    # Assert
    assert total == expected_total
    assert total == 200.5  # 10 + 25.5 + 50 + 15 + 100

def test_category_expense_summary():
    # Arrange
    """Test summary of expenses grouped by category."""
    df = pd.DataFrame([{
        "Amount": exp.amount,
        "Category": exp.category
    } for exp in sample_expenses])

    # Act
    summary = df.groupby("Category")["Amount"].sum().to_dict()

    expected_summary = {
        "Food": 25.0,           # 10 + 15
        "Transport": 25.5,
        "Entertainment": 50.0,
        "Bills": 100.0
    }

    # Assert
    assert summary == expected_summary