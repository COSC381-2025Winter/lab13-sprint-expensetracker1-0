import pytest
from expense import Expense
from expense_manager import SCOPES, load_expenses_from_sheets, authenticate_google_sheets, save_expenses_to_sheets, add_expense, view_expenses, delete_expense, expenses
import os
import builtins
from unittest.mock import patch, mock_open, MagicMock

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

# function test_authenticate_google_sheets_with_valid_token() developed using ChatGPT on 4/17/25
# prompt: "create test function for the following function (code from authenticate_google_sheets() included with prompt)"
@patch("expense_manager.os.path.exists")
@patch("expense_manager.Credentials.from_authorized_user_file")
@patch("expense_manager.build")
def test_authenticate_google_sheets_with_valid_token(mock_build, mock_from_auth_file, mock_exists):
    # Arrange
    mock_exists.return_value = True
    mock_creds = MagicMock()
    mock_creds.valid = True
    mock_from_auth_file.return_value = mock_creds
    mock_service = MagicMock()
    mock_build.return_value.spreadsheets.return_value = mock_service

    # Act
    result = authenticate_google_sheets()

    # Assert
    mock_from_auth_file.assert_called_once_with('token.json', SCOPES)
    mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_creds)
    assert result == mock_service

# function developed using ChatGPT on 04/17/25
# prompt "how to avoid using the real google sheets api when testing (save_expenses_to_sheets() code pasted here)"
@patch("expense_manager.authenticate_google_sheets")
def test_save_expenses_to_sheets(mock_auth):
    # Arrange
    e = Expense(20.5, "2025-04-14", "Groceries", "Fruits and snacks")
    add_expense(e)

    # Create fake Sheets API response
    fake_response = {
        "spreadsheetId": "some_id",
        "updatedRange": "Expenses!A2:D2",
        "updatedRows": 1
    }

    # Mock the Google Sheets service and its method chain
    mock_service = MagicMock()
    mock_service.values().update().execute.return_value = fake_response
    mock_auth.return_value = mock_service

    # Act
    save_response = save_expenses_to_sheets()

    # Assert
    assert "updatedRange" in save_response
    assert save_response["updatedRange"].startswith("Expenses!")

# function developed using ChatGPT on 04/17/25
# prompt "how to avoid using the real google sheets api when testing (load_expenses_from_sheets() code pasted here)"
@patch("expense_manager.authenticate_google_sheets")   # replace real api connection with fake one
def test_load_expenses_from_sheets_mocked(mock_auth):
    # Arrange
    fake_data = {
        'values': [
            ['2025-04-14', 'Groceries', 20.5, 'Fruits and snacks']
        ]
    }

    # Create a fake service with .values().get().execute() chain
    mock_service = MagicMock()
    mock_service.values().get.return_value.execute.return_value = fake_data
    mock_auth.return_value = mock_service

    # Act
    loaded_expenses = load_expenses_from_sheets()

    # Assert
    assert len(loaded_expenses) == 1
    assert loaded_expenses[0].category == 'Groceries'
    assert loaded_expenses[0].amount == 20.5
    assert loaded_expenses[0].description == 'Fruits and snacks'