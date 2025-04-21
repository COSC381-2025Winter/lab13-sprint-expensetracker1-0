from expense import Expense
from expense_manager import add_expense, view_expenses, save_expenses_to_sheets, load_expenses_from_sheets, sum_expenses

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
    
    # Add date filtering input
    start_date_str = input("Enter start date (YYYY-MM-DD, press Enter for no start date): ").strip()
    end_date_str = input("Enter end date (YYYY-MM-DD, press Enter for no end date): ").strip()

    # Use None if the input is empty, otherwise use the string
    start_date = start_date_str if start_date_str else None
    end_date = end_date_str if end_date_str else None

    print(f"\nDisplaying expenses" + (f" from {start_date}" if start_date else "") + (f" to {end_date}" if end_date else "") + ":")
    
    # Pass dates to view_expenses
    filtered_expenses = view_expenses(start_date=start_date, end_date=end_date)
    if filtered_expenses:
        for exp in filtered_expenses:
            print(exp)
        total = sum_expenses(start_date=start_date, end_date=end_date)
        print(f"\nTotal spent: "+
              (f" from {start_date}" if start_date else "")+
              (f" to {end_date}" if end_date else "")+
              f": ${total:.2f}")
    else:
        print("No expenses found within the specified date range.")


if __name__ == "__main__":
    main()
