import streamlit as st
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"


# Global state management
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

def save_token(token):
    """Save authentication token in session state"""
    st.session_state.access_token = token

def get_headers():
    """Returns authentication headers if user is logged in"""
    return {"Authorization": f"Bearer {st.session_state.access_token}"} if st.session_state.access_token else {}

### ✅ Authentication Functions
def login_user():
    """User login using JWT"""
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        payload = {"email": email, "password": password}
        response = requests.post(f"{BASE_URL}/auth/login/", json=payload)

        if response.status_code == 200:
            data = response.json()
            save_token(data["access"])
            st.success("Login successful!")
            st.session_state.user_email = email
        else:
            st.error(f"Login failed: {response.json()}")

def register_user():
    """User registration"""
    st.subheader("Register")
    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        payload = {"username": username, "email": email, "password": password}
        response = requests.post(f"{BASE_URL}/auth/register/", json=payload)

        if response.status_code == 201:
            st.success("Registration successful! Please log in.")
        else:
            st.error(f"Registration failed: {response.json()}")

### ✅ Dashboard View
def dashboard_view():
    """Fetch and display dashboard overview with structured UI"""
    st.subheader("📊 Dashboard Overview")

    response = requests.get(f"{BASE_URL}/dashboard/", headers=get_headers())

    if response.status_code == 200:
        data = response.json()
        st.write(f"👋 Welcome, **{data['message']}**")

        # Features Overview in a Grid
        st.write("### 🚀 Features Available")
        for category, links in data["features"].items():
            st.write(f"🔹 **{category}**")
            for feature, link in links.items():
                st.write(f"📌 {feature}: `{link}`")

    else:
        st.error("Failed to load dashboard.")


def create_user_profile():
    """Create a new user profile"""
    st.subheader("Create Profile")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    profile_picture = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])

    if st.button("Create Profile"):
        payload = {"full_name": full_name, "email": email}
        files = {"profile_picture": profile_picture} if profile_picture else {}

        response = requests.post(f"{BASE_URL}/dashboard/profile/create/", headers=get_headers(), json=payload, files=files)

        if response.status_code == 201:
            st.success("Profile created successfully!")
        else:
            st.error(f"Failed to create profile: {response.json()}")

### ✅ User Profile
def user_profile():
    """Fetch logged-in user's profile"""
    st.subheader("User Profile")
    response = requests.get(f"{BASE_URL}/dashboard/profile/", headers=get_headers())

    if response.status_code == 200:
        profile_data = response.json()
        st.json(profile_data)
    else:
        st.error(f"Failed to load profile: {response.json()}")

def update_user_profile():
    """Update user profile"""
    st.subheader("Update Profile")
    full_name = st.text_input("Full Name")

    if st.button("Update Profile"):
        payload = {"full_name": full_name}
        response = requests.put(f"{BASE_URL}/dashboard/profile/update/", headers=get_headers(), json=payload)

        if response.status_code == 200:
            st.success("Profile updated successfully!")
        else:
            st.error(f"Failed to update profile: {response.json()}")

###budget planning
def budget_entry():
    st.subheader("Enter Budget")
    income = st.number_input("Income")
    savings_goal = st.number_input("Savings Goal")
    month = st.date_input("Budget Month")
    budget_limit = st.number_input("Budget Limit")
    category = st.text_input("Category")

    if st.button("Submit Budget"):
        payload = {
            "income": income, "savings_goal": savings_goal, "month": month.strftime("%Y-%m-%d"),
            "budget_limit": budget_limit, "category": category
        }
        response = requests.post(f"{BASE_URL}/finance/budget/", headers=get_headers(), json=payload)

        if response.status_code == 201:
            st.success("Budget saved successfully!")
        else:
            st.error(f"Error saving budget: {response.json()}")

###transactions
def log_transaction():
    st.subheader("Log Transaction")
    amount = st.number_input("Amount", min_value=0.0)
    category = st.text_input("Category")
    transaction_date = st.date_input("Transaction Date")
    transaction_time = st.time_input("Transaction Time")
    merchant_name = st.text_input("Merchant Name")
    payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Card", "Net Banking"])
    transaction_description = st.text_input("Transaction Description")

    if st.button("Submit Transaction"):
        payload = {
            "amount": amount, "category": category, "transaction_date": transaction_date.strftime("%Y-%m-%d"),
            "transaction_time": transaction_time.strftime("%H:%M"), "merchant_name": merchant_name,
            "payment_method": payment_method, "transaction_description": transaction_description
        }
        response = requests.post(f"{BASE_URL}/finance/transactions/", headers=get_headers(), json=payload)

        if response.status_code == 201:
            st.success("Transaction added successfully!")
        else:
            st.error(f"Failed to log transaction: {response.json()}")

###recurring transaction
def recurring_transaction():
    """Log Recurring Transactions"""
    st.subheader("Recurring Transactions")
    
    amount = st.number_input("Amount", min_value=0.0)
    category = st.text_input("Category")
    start_date = st.date_input("Start Date")
    frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Yearly"])
    next_due_date = st.date_input("Next Due Date")
    merchant_name = st.text_input("Merchant Name")
    payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Card", "Net Banking"])

    if st.button("Submit Recurring Transaction"):
        payload = {
            "amount": amount, "category": category, "start_date": start_date.strftime("%Y-%m-%d"),
            "frequency": frequency, "next_due_date": next_due_date.strftime("%Y-%m-%d"),
            "merchant_name": merchant_name, "payment_method": payment_method
        }
        response = requests.post(f"{BASE_URL}/finance/recurring-transactions/", headers=get_headers(), json=payload)

        if response.status_code == 201:
            st.success("Recurring transaction saved successfully!")
        else:
            st.error(f"Failed to save recurring transaction: {response.json()}")

##fetch transactions
def list_transactions():
    """Fetch and display transactions (regular & recurring) in UI"""
    st.subheader("💳 Transaction History")

    response = requests.get(f"{BASE_URL}/finance/transactions/", headers=get_headers())
    recurring_response = requests.get(f"{BASE_URL}/finance/recurring-transactions/", headers=get_headers())

    if response.status_code == 200 and recurring_response.status_code == 200:
        transactions = response.json()
        recurring_transactions = recurring_response.json()

        if transactions or recurring_transactions:
            st.write("### Regular Transactions")
            st.table([
                [txn["transaction_date"], f"₹{txn['amount']}", txn["category"], txn["payment_method"]]
                for txn in transactions
            ])

            st.write("### Recurring Transactions")
            st.table([
                [r_txn["start_date"], f"₹{r_txn['amount']}", r_txn["category"], r_txn["frequency"], r_txn["next_due_date"]]
                for r_txn in recurring_transactions
            ])

        else:
            st.write("No transactions found.")

    else:
        st.error("Failed to fetch transactions.")

###financial_input_form
def financial_input_form():
    """Submit Financial Profile and Call AI Predictions"""
    st.subheader("Submit Financial Profile")

    with st.form("financial_profile"):
        income = st.number_input("income")
        age = st.number_input("Age", min_value=18, max_value=100)
        dependents = st.number_input("Dependents", min_value=0)
        occupation = st.text_input("Occupation")
        city_tier = st.selectbox("City Tier", [1, 2, 3])
        rent = st.number_input("Rent")
        loan_repayment = st.number_input("Loan Repayment")
        insurance = st.number_input("Insurance")
        groceries = st.number_input("Groceries")
        transport = st.number_input("Transport")
        eating_out = st.number_input("Eating Out")
        entertainment = st.number_input("Entertainment")
        utilities = st.number_input("Utilities")
        healthcare = st.number_input("Healthcare")
        education = st.number_input("Education")
        miscellaneous = st.number_input("Miscellaneous")
        savings_percentage = st.number_input("Desired Savings Percentage")

        submit = st.form_submit_button("Submit Profile")

        if submit:
            payload = {
                "income": income, "Age": age, "Dependents": dependents, "Occupation": occupation,
                "City_Tier": city_tier, "Rent": rent, "Loan_Repayment": loan_repayment, "Insurance": insurance,
                "Groceries": groceries, "Transport": transport, "Eating_Out": eating_out, "Entertainment": entertainment,
                "Utilities": utilities, "Healthcare": healthcare, "Education": education, "Miscellaneous": miscellaneous,
                "Desired_Savings_Percentage": savings_percentage
            }
            
            response = requests.post(f"{BASE_URL}/input-data/create/", headers=get_headers(), json=payload)

            if response.status_code == 201:
                st.success("Financial profile submitted successfully!")

                # AI Prediction Options
                st.subheader("Run AI Predictions")
                if st.button("Expense Breakdown"):
                    call_ai_prediction("expense-breakdown")
                if st.button("Overspending Alert"):
                    call_ai_prediction("overspending-alert")
                if st.button("Savings Efficiency"):
                    call_ai_prediction("savings-target-efficiency")
                if st.button("Anomaly Detection"):
                    call_ai_prediction("anomaly-detection")
                if st.button("Spending Recommendations"):
                    call_ai_prediction("recommendations")
                if st.button("Financial Health Score"):
                    call_ai_prediction("financial-health-score")

            else:
                st.error(f"Failed to submit profile: {response.json()}")

#finance_profile_view
def financial_profile_view():
    """Fetch financial profile details with UI formatting"""
    st.subheader("💰 Financial Profile")

    response = requests.get(f"{BASE_URL}/input-data/history/", headers=get_headers())

    if response.status_code == 200:
        profile = response.json()

        # Show financial data in a table
        st.write("### Financial Details")
        st.table([
            ["Income", f"₹{profile['income']}"],
            ["Age", profile["age"]],
            ["Occupation", profile["occupation"]],
            ["City Tier", profile["city_tier"]],
            ["Dependents", profile["dependents"]],
            ["Rent", f"₹{profile['rent']}"],
            ["Loan Repayment", f"₹{profile['loan_repayment']}"],
            ["Desired Savings %", f"{profile['desired_savings_percentage']}%"],
        ])

    else:
        st.error("Failed to fetch financial profile.")


### ✅ AI Predictions
def call_ai_prediction():
    """Fetch AI expense predictions"""
    st.subheader("AI Expense Prediction")
    prediction_type = st.selectbox("Prediction Type", ["expense", "anamoly", "overspending ","recommendation","savings","score"])

    if st.button("Generate Prediction"):
        payload = {"prediction_type": prediction_type}
        response = requests.post(f"{BASE_URL}/predict/", headers=get_headers(), json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success(f"Prediction Completed: {prediction_type}")
            st.write(f"Predicted Expense: {result['data'].get('predicted_expense', 'N/A')}")
            st.write(f"Confidence Score: {result['data'].get('confidence_score', 'N/A')}")
        else:
            st.error("Failed to generate prediction.")

###notifications
def fetch_notifications():
    """Fetch user notifications"""
    st.subheader("Your Notifications")
    
    response = requests.get(f"{BASE_URL}/finance/notifications/", headers=get_headers())
    
    if response.status_code == 200:
        notifications_list = response.json()

        if notifications_list:
            for notification in notifications_list:
                st.write(f"🔔 {notification['title']}: {notification['message']} (Read: {notification['read']})")
        else:
            st.write("No new notifications.")
    else:
        st.error("Failed to fetch notifications.")

def mark_notifications_as_read():
    """Mark notifications as read"""
    st.subheader("Mark Notifications as Read")
    
    response = requests.get(f"{BASE_URL}/finance/notifications/", headers=get_headers())

    if response.status_code == 200:
        notifications_list = response.json()
        
        if notifications_list:
            unread_notifications = [n for n in notifications_list if not n["read"]]
            ids_to_mark_read = [n["id"] for n in unread_notifications]

            if ids_to_mark_read:
                mark_payload = {"ids": ids_to_mark_read, "mark_as_read": True}
                update_response = requests.post(f"{BASE_URL}/finance/notifications/update/", headers=get_headers(), json=mark_payload)
                
                if update_response.status_code == 201:
                    st.success("Marked notifications as read!")
                else:
                    st.error("Failed to mark notifications as read.")
            else:
                st.write("All notifications are already read.")
        else:
            st.write("No notifications found.")
    else:
        st.error("Failed to fetch notifications.")

##report download csv/pdf
def download_reports():
    """Download CSV & PDF reports of transactions"""
    st.subheader("Download Reports")

    if st.button("Download CSV"):
        csv_response = requests.get(f"{BASE_URL}/export/csv/", headers=get_headers())

        if csv_response.status_code == 200:
            st.download_button("Download CSV", data=csv_response.content, file_name="transactions.csv")
        else:
            st.error("Failed to download CSV report.")

    if st.button("Download PDF"):
        pdf_response = requests.get(f"{BASE_URL}/export/pdf/", headers=get_headers())

        if pdf_response.status_code == 200:
            st.download_button("Download PDF", data=pdf_response.content, file_name="transactions.pdf")
        else:
            st.error("Failed to download PDF report.")


### ✅ Logout
def logout():
    """Log out user"""
    st.session_state.access_token = None
    st.session_state.user_email = ""
    st.success("Logged out successfully!")

### ✅ Main UI Navigation
def show_login_or_register():
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        login_user()
    with tab2:
        register_user()

st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💸 Finalyze")

# Sidebar navigation
menu = [
    "Login / Register", "Dashboard", "User Profile","Budget Setup", "Create Profile","Update Profile", "Transactions","Recurring Transactions",
    "list_transactions","Financial Profile Setup",'financial_profile_view', "AI Prediction", "Notifications", "Download Reports", "Logout"
]

choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login / Register":
    show_login_or_register()
elif st.session_state.access_token:
    if choice == "Dashboard":
        dashboard_view()
    elif choice == "User Profile":
        user_profile()
    elif choice == "Create Profile":
        create_user_profile()
    elif choice == "Update Profile":
        update_user_profile()
    elif choice == "Budget Setup":
        budget_entry()
    elif choice == "Transactions":
        log_transaction()
    elif choice == "Recurring Transactions":
         recurring_transaction()
    elif choice == "Recurring Transactions":
         list_transactions()
    elif choice == "Financial Profile Setup":
        financial_input_form()
    elif choice == 'financial_profile_view':
        financial_profile_view()
    elif choice == "AI Prediction":
        call_ai_prediction()
    elif choice == "Notifications":
        fetch_notifications()
    elif choice == "Download Reports":
        download_reports()
    elif choice == "Logout":
        logout()
else:
    st.warning("Please login/register to access this feature.")
