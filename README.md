# Expense Tracker

This is a simple expense tracker application.

## How to Run

1.  Clone the repository:
    ```bash
    git clone <https://github.com/COSC381-2025Winter/lab13-sprint-expensetracker1-0.git> 
    ```
    Replace `<repository_url>` with the actual URL of the repository.
2.  Make sure you have Python 3 and Streamlit installed. If not, install Streamlit using:
    ```bash
    pip install streamlit
    ```
3.  Install the other required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  To run the application, use the following command:
    ```bash
    streamlit run app.py
    ```
5.  Open your browser to the address shown in the terminal (usually `http://localhost:8501`).

## Google Sheets Integration

This application integrates with Google Sheets to store and retrieve expense data.

1.  You need to have a Google Cloud project set up with the Google Sheets API enabled.
2.  Download the `credentials.json` file from your Google Cloud project and place it in the same directory as the application.
3.  Run `python3 main.py` once to authenticate with Google Sheets. This will create a `token.json` file.

## Deployment

Deployment in this lab refers to packaging your project and uploading it to test.pypi.org.

1. Create and activate a new virtual environment.
2. Install the package in the virtual environment with this command:
    ```bash
    python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps lab13_Expense_t
    ```
3. After installation, run the program:
    ```bash
    python3 main.py
    streamlit run app.py
    ```
