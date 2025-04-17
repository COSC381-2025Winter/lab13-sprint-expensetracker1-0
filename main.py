from expense import Expense
from expense_manager import add_expense, view_expenses, save_expenses_to_sheets, load_expenses_from_sheets

# Example usage of expense tracker app with google sheets api integration
# Developed using perplexity.ai on 04/15/25
# Prompt: "could you please create a main method to test the usage example in python"
def main():
    # 1. Add local expenses
    print("Adding a new expense locally...")
    new_expense = Expense(25.50, "2024-04-14", "Food", "Lunch")
    new_expense2 = Expense(44.99, "2025-06-30", "Entertainment", "Movies")
    add_expense(new_expense)
    add_expense(new_expense2)
    print("Current local expenses:")
    for exp in view_expenses():
        print(exp)

    # 2. Save all local expenses to Google Sheets
    print("\nSaving expenses to Google Sheets...")
    save_response = save_expenses_to_sheets()
    print("Save response:", save_response)

    # 3. Clear local expenses and load from Google Sheets
    print("\nClearing local expenses and loading from Google Sheets...")
    global expenses
    expenses = []  # Clear local list
    loaded_expenses = load_expenses_from_sheets()
    print("Expenses loaded from Google Sheets:")
    for exp in loaded_expenses:
        print(exp)

if __name__ == "__main__":
    main()