import streamlit as st
import expense_manager
from datetime import datetime
import pandas as pd

# Set page title
st.set_page_config(page_title="Expense Tracker")

st.title("Expense Tracker")

# --- Add Expense Section ---
st.subheader("Add New Expense")
amount = st.number_input("Amount", min_value=0.00, format="%.2f")
date = st.date_input("Date", value=datetime.today())
category = st.text_input("Category")
description = st.text_input("Description")

def add_expense_to_list():
    try:
        if amount and date and category:
            expense_date_str = date.strftime("%Y-%m-%d")
            new_expense = expense_manager.Expense(amount, expense_date_str, category, description)
            expense_manager.add_expense(new_expense)
            st.success("Expense added successfully!")
            try:
                expense_manager.save_expenses_to_sheets()
                st.success("Expense saved to Google Sheets!")
            except Exception as e:
                st.error(f"An error occurred while saving: {e}")
            st.rerun() # Refresh the UI
        else:
            st.warning("Please fill in all required fields (Amount, Date, Category).")
    except ValueError:
        st.error("Invalid input for amount. Please enter a number.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if st.button("Add Expense"):
    add_expense_to_list()
    st.rerun() # Refresh the UI after adding expense

# --- Load and Save Expenses ---
if st.button("Save Expenses to Google Sheets"):
    try:
        expense_manager.save_expenses_to_sheets()
        st.success("Expenses saved to Google Sheets successfully!")
    except Exception as e:
        st.error(f"An error occurred while saving: {e}")
        st.warning("Please ensure 'credentials.json' is present and you have authenticated.")
        if not expense_manager.os.path.exists('token.json'):
            st.info("Run `python3 main.py` once in your terminal to authenticate with Google Sheets.")

# --- Load and Display Expenses ---
def display_expenses():
    try:
        # Load expenses from Google Sheets
        expenses = expense_manager.load_expenses_from_sheets()
        st.success("Expenses loaded successfully from Google Sheets.")

        # Date filtering
        st.subheader("Filter Expenses by Date")
        col1, col2 = st.columns(2)
        with col1:
            start_date_input = st.date_input("Start date", value=None, key="start_date")
        with col2:
            end_date_input = st.date_input("End date", value=None, key="end_date")

        # Convert dates to string format "YYYY-MM-DD" or None
        start_date_str = start_date_input.strftime("%Y-%m-%d") if start_date_input else None
        end_date_str = end_date_input.strftime("%Y-%m-%d") if end_date_input else None

        # Filter expenses using the manager function
        filtered_expenses = expense_manager.view_expenses(start_date=start_date_str, end_date=end_date_str)

        # Display filtered expenses
        st.subheader("Expenses")
        if filtered_expenses:
            # Prepare and display the DataFrame
            df = pd.DataFrame([{
                "Date": exp.date,
                "Category": exp.category,
                "Amount": exp.amount,
                "Description": exp.description
            } for exp in filtered_expenses])

            st.dataframe(df)

            # Calculating total expenses and summary by category developed using ChatGPT on 4/19/25
            # Prompt: "calculate total expenses over time and categorize spending with a calculation function. 
            #          (previous code block copy and pasted to show what we had to work with)"
            # --- Summary: Total Expenses ---
            st.subheader("Summary")
            total_amount = df["Amount"].sum()
            st.metric(label="Total Expenses", value=f"${total_amount:.2f}")

            # --- Summary by Category ---
            st.subheader("Expenses by Category")
            category_summary = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
            st.dataframe(category_summary.reset_index().rename(columns={"Amount": "Total Spent"}))
        else:
            st.write("No expenses found" + (f" between {start_date_str}" if start_date_str else "") + (f" and {end_date_str}" if end_date_str else "") + ".")

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.warning("Please ensure 'credentials.json' is present and you have authenticated.")
        # Offer authentication guidance if token is missing or invalid
        if not expense_manager.os.path.exists('token.json'):
             st.info("Run `python3 main.py` once in your terminal to authenticate with Google Sheets.")


# Initial display
display_expenses()

# Refresh button
if st.button("Refresh Data"):
    st.rerun()
