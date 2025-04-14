from expense import Expense

expenses = []

def add_expense(expense):
    if not isinstance(expense, Expense):
        raise TypeError("Expected an Expense object")
    expenses.append(expense)

def view_expenses():
    return expenses

def delete_expense(index):
    if 0 <= index < len(expenses):
        del expenses[index]
        return True
    return False
