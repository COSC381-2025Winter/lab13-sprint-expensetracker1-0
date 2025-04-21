from expense import Expense
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

# Existing expense list functions
expenses = []

# Google Sheets Configuration
# Developed using perplexity.ai on 04/15/25
# Prompt: "We would like to integrate google sheets api with our program to do the following:
#          - Set up google sheets API authentication
#          - Create functions to save expenses to google sheets
#          - implement function to retrieve stored expense"
# Also added the code from expense_manager.py and expense.py to the prompt
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1NIVI1BIsiwnP2R54OLuPjAzvgCYoy-l-V3T2l1jBZSQ'
RANGE_NAME = 'Sheet1!A2:D'

def authenticate_google_sheets():
    """Handles OAuth2 authentication"""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('sheets', 'v4', credentials=creds).spreadsheets()

def save_expenses_to_sheets():
    """Saves all expenses to Google Sheets, starting at row 2 to preserve the header."""
    service = authenticate_google_sheets()
    values = [
        [exp.date, exp.category, exp.amount, exp.description]
        for exp in expenses
    ]
    body = {'values': values}
    request = service.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,  # Now starts at A2
        valueInputOption='RAW',
        body=body
    )
    response = request.execute()
    return response

def load_expenses_from_sheets():
    """Loads expenses from Google Sheets"""
    service = authenticate_google_sheets()
    
    result = service.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()

    global expenses
    expenses = [
        Expense(
            amount=row[2],
            date=row[0],
            category=row[1],
            description=row[3] if len(row) > 3 else ""
        ) for row in result.get('values', [])
    ]
    return expenses

def add_expense(expense):
    if not isinstance(expense, Expense):
        raise TypeError("Expected an Expense object")
    expenses.append(expense)

def view_expenses(start_date=None, end_date=None):
    """Returns a list of expenses, optionally filtered by date range."""
    if not start_date and not end_date:
        return expenses  # Return all if no dates are specified

    filtered_expenses = []
    for expense in expenses:
        # Assume date format is "YYYY-MM-DD" and compare as strings
        if start_date and expense.date < start_date:
            continue
        if end_date and expense.date > end_date:
            continue
        filtered_expenses.append(expense)
    
    return filtered_expenses

def delete_expense(index):
    if 0 <= index < len(expenses):
        del expenses[index]
        return True
    return False

def sum_expenses(start_date=None, end_date=None):
    filtered = view_expenses(start_date=start_date, end_date=end_date)
    return sum(exp.amount for exp in filtered)