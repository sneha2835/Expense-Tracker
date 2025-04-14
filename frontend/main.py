import streamlit as st
import requests
import json
from datetime import date

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
import streamlit as st
import requests
import webbrowser


def dashboard_view():
    """Fetch and display dashboard overview with structured UI"""
    st.subheader("📊 Dashboard Overview")

    response = requests.get(f"{BASE_URL}/dashboard/", headers=get_headers())

    if response.status_code == 200:
        data = response.json()
        st.write(f"👋  **{data['message']}**")

        # Initialize main control state
        if "active_section" not in st.session_state:
            st.session_state.active_section = None

        # Section: MAIN MENU
        if st.session_state.active_section is None:
            st.markdown("### 🔽 Select a Feature to Continue")
            if st.button("👤 Your Profile"):
                st.session_state.active_section = "profile"
            if st.button("💸 Budget Setup"):
                st.session_state.active_section = "budget"
            if st.button("💳 Transactions"):
                st.session_state.active_section = "transactions"
            if st.button("🤖 AI Predictions"):
                st.session_state.active_section = "ai"
            if st.button("Logout"):
                logout()

        # Section: PROFILE
        elif st.session_state.active_section == "profile":
            if "active_profile_action" not in st.session_state:
                st.session_state.active_profile_action = None

            st.markdown("### 🔧 Profile Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👁️ View Profile"):
                    st.session_state.active_profile_action = "view"
            with col2:
                if st.button("➕ Create Profile"):
                    st.session_state.active_profile_action = "create"

            col3, col4 = st.columns(2)
            with col3:
                if st.button("✏️ Update Profile"):
                    st.session_state.active_profile_action = "update"
            with col4:
                if st.button("🗑️ Delete Profile"):
                    st.session_state.active_profile_action = "delete"

            if st.session_state.active_profile_action == "create":
                create_user_profile()
            elif st.session_state.active_profile_action == "view":
                view_user_profile()
            elif st.session_state.active_profile_action == "update":
                update_user_profile()
            elif st.session_state.active_profile_action == "delete":
                delete_user_profile()

            if st.button("🔙 Back to Dashboard"):
                st.session_state.active_section = None
                st.session_state.active_profile_action = None

        # Section: BUDGET
        elif st.session_state.active_section == "budget":
            if "active_budget_action" not in st.session_state:
                st.session_state.active_budget_action = None

            st.markdown("### 🧾 Budget Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("➕ Enter Budget"):
                    st.session_state.active_budget_action = "enter"
            with col2:
                if st.button("✏️ Update Budget"):
                    st.session_state.active_budget_action = "update"

            col3, col4 = st.columns(2)
            with col3:
                if st.button("👁️ View Budget"):
                    st.session_state.active_budget_action = "view"
            with col4:
                if st.button("🗑️ Delete Budget"):
                    st.session_state.active_budget_action = "delete"

            if st.session_state.active_budget_action == "enter":
                enter_budget()
            elif st.session_state.active_budget_action == "update":
                update_budget()
            elif st.session_state.active_budget_action == "view":
                view_budget()
            elif st.session_state.active_budget_action == "delete":
                delete_budget()

            if st.button("🔙 Back to Dashboard"):
                st.session_state.active_section = None
                st.session_state.active_budget_action = None

        # Section: TRANSACTIONS
        elif st.session_state.active_section == "transactions":
            if "active_transaction_action" not in st.session_state:
                st.session_state.active_transaction_action = None

            st.markdown("### 🔧 Transaction Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Log Transaction"):
                    st.session_state.active_transaction_action = "log"
            with col2:
                if st.button("🔁 Recurring Transactions"):
                    st.session_state.active_transaction_action = "recurring"

            col3, col4 = st.columns(2)
            with col3:
                if st.button("📜 List Transactions"):
                    st.session_state.active_transaction_action = "list"
            with col4:
                if st.button("📥 Download Reports"):
                    st.session_state.active_transaction_action = "download"

            if st.session_state.active_transaction_action == "log":
                log_transaction()
            elif st.session_state.active_transaction_action == "recurring":
                recurring_transaction()
            elif st.session_state.active_transaction_action == "list":
                list_transactions()
            elif st.session_state.active_transaction_action == "download":
                download_reports()

            if st.button("🔙 Back to Dashboard"):
                st.session_state.active_section = None
                st.session_state.active_transaction_action = None

        # Section: AI PREDICTIONS
        elif st.session_state.active_section == "ai":
            if "active_ai_prediction_action" not in st.session_state:
                st.session_state.active_ai_prediction_action = None

            st.markdown("### 💡 AI Prediction Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Financial Profile Setup"):
                    st.session_state.active_ai_prediction_action = "profile_setup"
            with col2:
                if st.button("🔎 Financial Profile View"):
                    st.session_state.active_ai_prediction_action = "profile_view"

            col3, col4 = st.columns(2)
            with col3:
                if st.button("Expense Breakdown"):
                    call_ai_prediction("expense-breakdown")
            with col4:
                if st.button("Overspending Alert"):
                    call_ai_prediction("overspending-alert")

            col5, col6 = st.columns(2)
            with col5:
                if st.button("Savings Efficiency"):
                    call_ai_prediction("savings-target-efficiency")
            with col6:
                if st.button("Anomaly Detection"):
                    call_ai_prediction("anomaly-detection")

            col7, col8 = st.columns(2)
            with col7:
                if st.button("Spending Recommendations"):
                    call_ai_prediction("recommendations")
            with col8:
                if st.button("Financial Health Score"):
                    call_ai_prediction("financial-health-score")

            if st.session_state.active_ai_prediction_action == "profile_setup":
                financial_input_form()
            elif st.session_state.active_ai_prediction_action == "profile_view":
                financial_profile_view()

            if st.button("🔙 Back to Dashboard"):
                st.session_state.active_section = None
                st.session_state.active_ai_prediction_action = None

    else:
        st.error("Failed to load dashboard.")



### ✅ User Profile
def view_user_profile():
    """View user profile with styled layout"""
    st.subheader("👁️ View Profile")

    response = requests.get(f"{BASE_URL}/dashboard/profile/", headers=get_headers())
    
    if response.status_code == 200:
        data = response.json()

        st.markdown("### 👤 Profile Details")

        profile_pic_url = data.get("profile_picture")  # Adjust if your backend uses a different key

        col1, col2 = st.columns([1, 2])

        with col1:
            if profile_pic_url:
                st.image(profile_pic_url, width=150, caption="Profile Picture")
            else:
                st.image("https://via.placeholder.com/150", width=150, caption="No Picture")

        with col2:
            st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                    <h4 style="margin-bottom: 0.5rem;">Full Name: <span style="color: #3c4043;">{data.get('full_name', 'N/A')}</span></h4>
                    <p style="margin: 0;">User ID: <strong>{data.get('user', 'N/A')}</strong></p>
                    <p style="margin: 0;">Profile ID: <strong>{data.get('id', 'N/A')}</strong></p>
                </div>
            """, unsafe_allow_html=True)

        # Optional: Button to go to update profile
        if st.button("✏️ Edit Profile"):
            st.session_state.active_profile_action = "Update Profile"

    elif response.status_code == 404:
        st.warning("No profile found. Please create one first.")
    else:
        st.error("Failed to fetch profile.")


def update_user_profile():
    """Update existing user profile"""
    st.subheader("✏️ Update Profile")

    response = requests.get(f"{BASE_URL}/dashboard/profile/", headers=get_headers())
    if response.status_code != 200:
        st.error("Failed to load current profile.")
        return

    data = response.json()

    full_name = st.text_input("Full Name", value=data.get("full_name", ""))
    email = st.text_input("Email", value=data.get("email", ""))
    profile_picture = st.file_uploader("Upload New Profile Picture", type=["jpg", "png"])

    if st.button("Update Profile"):
        payload = {"full_name": full_name, "email": email}

        if profile_picture:
            files = {"profile_picture": (profile_picture.name, profile_picture, profile_picture.type)}
            response = requests.put(
                f"{BASE_URL}/dashboard/profile/update/",
                headers=get_headers(),
                data=payload,
                files=files
            )
        else:
            response = requests.put(
                f"{BASE_URL}/dashboard/profile/update/",
                headers=get_headers(),
                json=payload
            )

        if response.status_code == 200:
            st.success("✅ Profile updated successfully!")
            st.session_state.active_profile_action = None
        else:
            st.error(f"❌ Update failed: {response.text}")

def delete_user_profile():
    """Delete user profile"""
    st.subheader("🗑️ Delete Profile")

    confirm = st.checkbox("I really want to delete my profile")
    if confirm and st.button("Delete Now"):
        response = requests.delete(f"{BASE_URL}/dashboard/profile/delete/", headers=get_headers())

        if response.status_code == 204:
            st.success("🧹 Profile deleted successfully!")
            st.session_state.active_profile_action = None
        else:
            st.error(f"❌ Deletion failed: {response.text}")


###budget planning


def get_headers():
    token = st.session_state.get("access_token", "")
    return {"Authorization": f"Bearer {token}"}

# Individual Budget Functions
def enter_budget():
    st.subheader("Enter Budget")
    income = st.number_input("Income")
    savings_goal = st.number_input("Savings Goal")
    month = st.date_input("Budget Month", value=date.today())
    budget_limit = st.number_input("Budget Limit")
    category = st.text_input("Category")

    if st.button("Submit Budget"):
        payload = {
            "income": income,
            "savings_goal": savings_goal,
            "month": month.strftime("%Y-%m-%d"),
            "budget_limit": budget_limit,
            "category": category,
        }
        response = requests.post(f"{BASE_URL}/finance/budget/", headers=get_headers(), json=payload)

        if response.status_code == 201:
            st.success("Budget saved successfully!")
        else:
            st.error(f"Error saving budget: {response.text}")

def update_budget():
    st.subheader("Update Budget")
    budget_id = st.text_input("Enter Budget ID to update")
    income = st.number_input("New Income")
    savings_goal = st.number_input("New Savings Goal")
    budget_limit = st.number_input("New Budget Limit")
    category = st.text_input("New Category")
    month = st.date_input("New Budget Month", value=date.today())

    if st.button("Update Budget"):
        payload = {
            "income": income,
            "savings_goal": savings_goal,
            "month": month.strftime("%Y-%m-%d"),
            "budget_limit": budget_limit,
            "category": category,
        }
        response = requests.put(f"{BASE_URL}/finance/budget/{budget_id}/", headers=get_headers(), json=payload)
        if response.status_code in [200, 202]:
            st.success("Budget updated successfully!")
        else:
            st.error(f"Error updating budget: {response.text}")


def view_budget():
    st.subheader("💼 View Budget")
    
    # ✅ Step 1: Print token to debug
    st.write("Access Token:", st.session_state.access_token)
    
    # Then make your API call
    response = requests.get(f"{BASE_URL}/budget/view/", headers=get_headers())


    if response.status_code == 200:
        data = response.json()

        # Optional: If API returns a list, get the first item
        if isinstance(data, list):
            budget = data[0] if data else None
        else:
            budget = data

        if not budget:
            st.warning("No budget data available.")
            return

        st.markdown(
            f"""
            <div style="background-color:#f0f2f6; padding:20px; border-radius:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <h4 style="margin-bottom:10px;">📅 Month: {budget['month']}</h4>
                <p><strong>💰 Income:</strong> ₹{float(budget['income']):,.2f}</p>
                <p><strong>🎯 Savings Goal:</strong> ₹{float(budget['savings_goal']):,.2f}</p>
                <p><strong>🧾 Budget Limit:</strong> ₹{float(budget['budget_limit']):,.2f}</p>
                <p><strong>🏷️ Category:</strong> {budget['category'].capitalize()}</p>
                <p><strong>🕒 Created At:</strong> {datetime.strptime(budget['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b %d, %Y %I:%M %p")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.error("❌ Failed to fetch budget data.")


def delete_budget():
    st.subheader("Delete Budget")
    budget_id = st.text_input("Enter Budget ID to delete")
    if st.button("Delete Budget"):
        response = requests.delete(f"{BASE_URL}/finance/budget/{budget_id}/", headers=get_headers())
        if response.status_code == 204:
            st.success("Budget deleted successfully!")
        else:
            st.error(f"Error deleting budget: {response.text}")

###transactions
def transactions_section():
    """Transactions Section (Regular, Recurring, List, Download)"""
    
    # Transactions Expander
    with st.expander("🔄 Transactions"):
        log_transaction()

    # Recurring Transactions Expander
    with st.expander("🔁 Recurring Transactions"):
        recurring_transaction()

    # List Transactions Expander
    with st.expander("📜 List Transactions"):
        list_transactions()

    # Download Reports Expander
    with st.expander("📥 Download Reports"):
        download_reports()

# --- Log Transaction ---
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

# --- Recurring Transaction ---
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

# --- List Transactions ---
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
            st.table([[
                txn["transaction_date"], f"₹{txn['amount']}", txn["category"], txn["payment_method"]
            ] for txn in transactions])

            st.write("### Recurring Transactions")
            st.table([[
                r_txn["start_date"], f"₹{r_txn['amount']}", r_txn["category"], r_txn["frequency"], r_txn["next_due_date"]
            ] for r_txn in recurring_transactions])

        else:
            st.write("No transactions found.")

    else:
        st.error("Failed to fetch transactions.")

###financial_input_form
def financial_input_form():
    """Submit Financial Profile and Call AI Predictions"""
    st.subheader("Submit Financial Profile")

    with st.form("financial_profile"):
        income = st.number_input("Income")
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
                st.session_state.active_ai_prediction_action = "profile_view"  # Auto redirect to view profile
            else:
                try:
                    error_detail = response.json()
                except ValueError:
                     if "Duplicate entry" in response.text:
                        error_detail = "A profile already exists for this user. Please update it instead."
                     else:
                        error_detail = response.text or "No response body or invalid JSON returned from server."
                st.error(f"Failed to submit profile: {error_detail}") 
### Financial Profile View
def financial_profile_view():
    """Fetch financial profile details with UI formatting"""
    st.subheader("💰 Financial Profile")

    response = requests.get(f"{BASE_URL}/input-data/history/", headers=get_headers())

    if response.status_code == 200:
        profile = response.json()
        if profile:
            profile = profile[0]

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
                ["Desired Savings %", f"{profile.get('desired_savings_percentage', 'N/A')}%"],
            ])
        else:
            st.warning("No financial profile found.")
    else:
        st.error("Failed to fetch financial profile.")



### ✅ AI Predictions
def call_ai_prediction(prediction_type):
    """Fetch AI expense predictions and display results"""
    st.subheader(f"AI Prediction: {prediction_type.capitalize()}")

    payload = {"prediction_type": prediction_type}
    response = requests.post(f"{BASE_URL}/predict/", headers=get_headers(), json=payload)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction Completed: {prediction_type.capitalize()}")
        st.write(f"Predicted Expense: {result['data'].get('predicted_expense', 'N/A')}")
        st.write(f"Confidence Score: {result['data'].get('confidence_score', 'N/A')}")
    else:
        st.error("Failed to generate prediction.")
        
        # 🔍 Debug info
        st.code(f"Status Code: {response.status_code}", language="text")
        try:
            st.code(response.json(), language="json")
        except ValueError:
            st.code(response.text or "No error message returned.", language="text")



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


# Sidebar navigation
if not st.session_state.access_token:
    menu = [
        "Login / Register", "Dashboard"
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login / Register":
        show_login_or_register()
    elif choice == "Logout":
        logout()
else:
    # Hide the sidebar once the user is logged in
    st.sidebar.empty()

    # Show dashboard after login
    dashboard_view()