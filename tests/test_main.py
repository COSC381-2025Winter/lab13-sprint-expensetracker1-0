import pytest 
from main import main
from unittest.mock import patch, MagicMock

def test_print_messages(capsys, mocker):
    # Arrange
    # Mock the Google Sheets API service to avoid real API calls
    mock_service = MagicMock()
    mocker.patch("expense_manager.authenticate_google_sheets", return_value=mock_service)

    # Act
    main()
    captured = capsys.readouterr()

    # Assert
    assert "Adding a new expense locally..." in captured.out
    assert "Current local expenses:" in captured.out
    assert "\nSaving expenses to Google Sheets..." in captured.out
    assert "Save response:" in captured.out
    assert "\nClearing local expenses and loading from Google Sheets..." in captured.out
    assert "Expenses loaded from Google Sheets:" in captured.out
    