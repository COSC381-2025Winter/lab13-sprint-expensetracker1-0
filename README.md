# Expense Tracker

This is a simple expense tracker application.

## How to Run

1.  **Clone the Repository**  
    Clone the GitHub repository to your local machine:
    ```bash
    git clone https://github.com/COSC381-2025Winter/lab13-sprint-expensetracker1-0.git
    ```
2.  **Install Python 3 and Streamlit**  
    Make sure you have Python 3 installed. Then, install Streamlit using:
    ```bash
    pip install streamlit
    ```
3.  **Install Required Packages**  
    Install the other required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Application**  
    Start the application with the following command:
    ```bash
    streamlit run app.py
    ```
5.  **Open the App in Your Browser**  
    Open your browser to the address shown in the terminal (usually `http://localhost:8501`).

## Google Sheets Integration

This application integrates with Google Sheets to store and retrieve expense data.

1.  You need to have a Google Cloud project set up with the Google Sheets API enabled.
2.  Download the `credentials.json` file from your Google Cloud project and place it in the same directory as the application.
3.  Run `python3 main.py` once to authenticate with Google Sheets. This will create a `token.json` file.

## Deployment

1.  Create and activate a new virtual environment.
2.  Install the package in the virtual environment with this command:
    ```bash
    python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps lab13_Expense_tracker_W381 --upgrade
    ```
