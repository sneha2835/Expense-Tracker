import streamlit as st
import requests
import json
from datetime import date,datetime

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
            try:
                error_msg = response.json()
            except ValueError:
                error_msg = response.text
            st.error(f"Login failed: {error_msg}")

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
            st.markdown("### 💡 AI Prediction Actions")

            col1, col2 = st.columns(2)
            with col1:
                with st.expander("📊 Expense Prediction", expanded=True):
                    expense_prediction_form()
            with col2:
                with st.expander("🚨 Overspending Alert",expanded=True):
                    overspending_alert_form()

            col3, col4 = st.columns(2)
            with col3:
                with st.expander("🔍 Anomaly Detection",expanded=True):
                    anomaly_detection_form()
            with col4:
                with st.expander("💰 Savings Efficiency",expanded=True):
                    savings_efficiency_form()
            col5, col6 = st.columns(2)
            with col5:
                with st.expander("📈 Financial Score",expanded=True):
                    financial_score_form() 
            with col6:
                with st.expander("💡 Personalized Recommendations",expanded=True):
                    personalized_recommendation_form()
            
            


            if st.button("🔙 Back to Dashboard"):
                st.session_state.active_section = None

    else:
        st.error("Failed to load dashboard.")

def create_user_profile():
    """Create a new user profile"""
    st.subheader("➕ Create Profile")

    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    profile_picture = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])

    if st.button("Submit Profile"):
        payload = {"full_name": full_name, "email": email}
        
        # Check file and use appropriate request structure
        if profile_picture:
            # Multipart with file
            files = {"profile_picture": (profile_picture.name, profile_picture, profile_picture.type)}
            response = requests.post(
                f"{BASE_URL}/dashboard/profile/create/",
                headers=get_headers(),
                data=payload,
                files=files
            )
        else:
            # JSON without file
            response = requests.post(
                f"{BASE_URL}/dashboard/profile/create/",
                headers=get_headers(),
                json=payload
            )

        if response.status_code == 201:
            st.success("✅ Profile created successfully!")
            st.session_state.active_profile_action = None  # Reset view
        else:
            st.error(f"❌ Failed to create profile: {response.text}")


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
    st.subheader("📊 Enter Budget")
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
            budget = response.json()
            st.session_state.budget_id = budget["id"]  # Save for later use

            st.markdown(
                f"""
                    <div style="background-color:#ffffff; color:#000000; padding:20px; border-radius:12px; border:1px solid #dcdcdc; box-shadow: 0 2px 6px rgba(0,0,0,0.05); font-family:Arial, sans-serif;">                    
                    <h4>✅ Budget Created Successfully!</h4>
                    <p><strong>📌 Budget ID:</strong> <code>{budget['id']}</code></p>
                    <p><strong>💰 Income:</strong> ₹{float(budget['income']):,.2f}</p>
                    <p><strong>🎯 Savings Goal:</strong> ₹{float(budget['savings_goal']):,.2f}</p>
                    <p><strong>🧾 Budget Limit:</strong> ₹{float(budget['budget_limit']):,.2f}</p>
                    <p><strong>🏷️ Category:</strong> {budget['category'].capitalize()}</p>
                    <p><strong>🗓️ Month:</strong> {budget['month']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error(f"🚫 Error saving budget: {response.text}")

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

    # Make GET request to the API to fetch the current user's budgets
    response = requests.get(f"{BASE_URL}/finance/budget/", headers=get_headers())

    # Check if response status is 200 (Success)
    if response.status_code == 200:
        budgets = response.json()

        # If there are no budgets, inform the user
        if not budgets:
            st.warning("You don't have any budgets yet.")

        # If there are budgets, display them
        else:
            for budget in budgets:
                st.markdown(
                    f"""
                    <div style="background-color:#ffffff; color:#000000; padding:20px; 
                                border-radius:12px; border:1px solid #dcdcdc; 
                                box-shadow: 0 2px 6px rgba(0,0,0,0.05); font-family:Arial, sans-serif;">
                        <h4 style="margin-bottom:10px;">📄 Budget Details</h4>
                        <p><strong>📌 Budget ID:</strong> <code>{budget['id']}</code></p>
                        <p><strong>💰 Income:</strong> ₹{float(budget['income']):,.2f}</p>
                        <p><strong>🎯 Savings Goal:</strong> ₹{float(budget['savings_goal']):,.2f}</p>
                        <p><strong>🧾 Budget Limit:</strong> ₹{float(budget['budget_limit']):,.2f}</p>
                        <p><strong>🏷️ Category:</strong> {budget['category'].capitalize()}</p>
                        <p><strong>🗓️ Month:</strong> {budget['month']}</p>
                        <p><strong>🕒 Created At:</strong> {datetime.strptime(budget['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b %d, %Y %I:%M %p")}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Handle errors
    elif response.status_code == 401:
        st.error("❌ Unauthorized: Please check your token or login again.")
    else:
        st.error(f"❌ Something went wrong: {response.status_code} - {response.text}")
        st.write(f"API Response: {response.json()}")  # Display the response for debugging

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
    
    # Dropdown for categories
    categories = [
        "Rent", "Loan_Repayment", "Insurance", "Groceries", "Transport", "Eating_Out", 
        "Entertainment", "Utilities", "Healthcare", "Education", "Miscellaneous"
    ]
    category = st.selectbox("Category", categories)
    
    transaction_date = st.date_input("Transaction Date")
    transaction_time = st.time_input("Transaction Time")
    merchant_name = st.text_input("Merchant Name")
    payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Card", "Net Banking"])
    transaction_description = st.text_input("Transaction Description")

    if st.button("Submit Transaction"):
        payload = {
            "amount": amount,
            "category": category,
            "transaction_date": transaction_date.strftime("%Y-%m-%d"),
            "transaction_time": transaction_time.strftime("%H:%M"),
            "merchant_name": merchant_name,
            "payment_method": payment_method,
            "transaction_description": transaction_description
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
    
    # Dropdown for categories
    categories = [
        "Rent", "Loan_Repayment", "Insurance", "Groceries", "Transport", "Eating_Out", 
        "Entertainment", "Utilities", "Healthcare", "Education", "Miscellaneous"
    ]
    category = st.selectbox("Category", categories)
    
    start_date = st.date_input("Start Date")
    frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Yearly"])
    next_due_date = st.date_input("Next Due Date")
    merchant_name = st.text_input("Merchant Name")
    payment_method = st.selectbox("Payment Method", ["Cash", "UPI", "Card", "Net Banking"])

    if st.button("Submit Recurring Transaction"):
        payload = {
            "amount": amount,
            "category": category,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "frequency": frequency,
            "next_due_date": next_due_date.strftime("%Y-%m-%d"),
            "merchant_name": merchant_name,
            "payment_method": payment_method
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
            # Display Regular Transactions
            st.write("### Regular Transactions")
            regular_transactions = [
                ["Date", "Amount", "Category", "Payment Method"]  # Header row, no row numbers
            ]
            for txn in transactions:
                regular_transactions.append([
                    txn["transaction_date"], 
                    f"₹{txn['amount']}", 
                    txn["category"], 
                    txn["payment_method"]
                ])

            st.table(regular_transactions)  # Just pass the list with headers as the first row

            # Display Recurring Transactions
            st.write("### Recurring Transactions")
            recurring_transactions_list = [
                ["Start Date", "Amount", "Category", "Frequency", "Next Due Date"]  # Header row, no row numbers
            ]
            for r_txn in recurring_transactions:
                recurring_transactions_list.append([
                    r_txn["start_date"], 
                    f"₹{r_txn['amount']}", 
                    r_txn["category"], 
                    r_txn["frequency"], 
                    r_txn["next_due_date"]
                ])

            st.table(recurring_transactions_list)  # Just pass the list with headers as the first row

        else:
            st.write("No transactions found.")

    else:
        st.error("❌ Failed to fetch transactions.")
def send_request(endpoint, payload):
    import requests

    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}",
        "Content-Type": "application/json"
    }

    url = f"http://127.0.0.1:8000/api/{endpoint}/"  # Make sure this URL matches your actual backend route

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()  # ✅ This is what your code needs!
        else:
            st.error(f"API Error: {response.status_code}")
            st.write("🚨 Response Text:", response.text)
            return None
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None


def expense_prediction_form():
    st.subheader("📊 Expense Prediction")
    with st.form("expense_prediction"):
        income = st.number_input("Income", min_value=0)
        age = st.number_input("Age", min_value=0)
        dependents = st.number_input("Dependents", min_value=0)
        occupation = st.text_input("Occupation")
        city_tier = st.number_input("City Tier", min_value=1, max_value=3)

        rent = st.number_input("Rent", min_value=0)
        loan_repayment = st.number_input("Loan Repayment", min_value=0)
        insurance = st.number_input("Insurance", min_value=0)
        groceries = st.number_input("Groceries", min_value=0)
        transport = st.number_input("Transport", min_value=0)
        eating_out = st.number_input("Eating Out", min_value=0)
        entertainment = st.number_input("Entertainment", min_value=0)
        utilities = st.number_input("Utilities", min_value=0)
        healthcare = st.number_input("Healthcare", min_value=0)
        education = st.number_input("Education", min_value=0)
        miscellaneous = st.number_input("Miscellaneous", min_value=0)

        savings = st.number_input("Desired Savings Percentage", min_value=0, max_value=100)

        submit = st.form_submit_button("Predict Expense Breakdown")

    if submit:
        st.write("✅ Submit triggered, sending request...")  # DEBUG LINE
        payload = {
            "Income": income,
            "Age": age,
            "Dependents": dependents,
            "Occupation": occupation,
            "City_Tier": city_tier,
            "Rent": rent,
            "Loan_Repayment": loan_repayment,
            "Insurance": insurance,
            "Groceries": groceries,
            "Transport": transport,
            "Eating_Out": eating_out,
            "Entertainment": entertainment,
            "Utilities": utilities,
            "Healthcare": healthcare,
            "Education": education,
            "Miscellaneous": miscellaneous,
            "Desired_Savings_Percentage": savings
        }

        response = send_request("predict/expense", payload)

        if response:
            st.success("✅ Prediction successful!")
            prediction = response.get("Expense_Prediction", {})
            st.write("### 🔍 Prediction Output")
            st.write("**Disposable Income:**", prediction.get("Disposable_Income"))
            st.write("**Total Expenses:**", prediction.get("Total_Expenses"))
            st.write("**Category-wise Breakdown:**")
            category_expenses = prediction.get("Category_Expenses", {})
            for category, amount in category_expenses.items():
                st.markdown(f"- **{category}:** ₹{amount:,.2f}")
        else:
            st.error("❌ Failed to get prediction.")

def overspending_alert_form():
    st.subheader("🚨 Overspending Alert")
    with st.form("overspending_alert"):
        income = st.number_input("Income", min_value=0)
        age = st.number_input("Age", min_value=0)
        dependents = st.number_input("Dependents", min_value=0)
        occupation = st.text_input("Occupation")
        city_tier = st.number_input("City Tier", min_value=1, max_value=3)

        rent = st.number_input("Rent", min_value=0)
        loan_repayment = st.number_input("Loan Repayment", min_value=0)
        insurance = st.number_input("Insurance", min_value=0)
        groceries = st.number_input("Groceries", min_value=0)
        transport = st.number_input("Transport", min_value=0)
        eating_out = st.number_input("Eating Out", min_value=0)
        entertainment = st.number_input("Entertainment", min_value=0)
        utilities = st.number_input("Utilities", min_value=0)
        healthcare = st.number_input("Healthcare", min_value=0)
        education = st.number_input("Education", min_value=0)
        miscellaneous = st.number_input("Miscellaneous", min_value=0)

        savings = st.number_input("Desired Savings Percentage", min_value=0, max_value=100)

        submit = st.form_submit_button("Check Overspending Risk")

    if submit:
        st.write("🔄 Submitting for overspending analysis...")
        payload = {
            "Income": income,
            "Age": age,
            "Dependents": dependents,
            "Occupation": occupation,
            "City_Tier": city_tier,
            "Rent": rent,
            "Loan_Repayment": loan_repayment,
            "Insurance": insurance,
            "Groceries": groceries,
            "Transport": transport,
            "Eating_Out": eating_out,
            "Entertainment": entertainment,
            "Utilities": utilities,
            "Healthcare": healthcare,
            "Education": education,
            "Miscellaneous": miscellaneous,
            "Desired_Savings_Percentage": savings
        }

        response = send_request("predict/overspending", payload)

        if response is not None:
            st.success("✅ Overspending analysis successful!")

            alert = response.get("Overspending_Alert", None)

            st.write("### 🔍 Overspending Insight")
            
            if isinstance(alert, dict):
                # Show it like a catalog
                st.markdown(f"""
                - **Risk Level:** {alert.get('Risk_Level', 'N/A')}
                - **Message:** {alert.get('Message', 'No message provided')}
                """)
            elif alert is False:
                st.info("🎉 You're spending wisely. No overspending risk detected!")
            else:
                st.warning("⚠️ Could not interpret the response.")
        else:
            st.error("❌ Failed to get overspending prediction.")



def anomaly_detection_form():
    st.subheader("🔍 Anomaly Detection")
    with st.form("anomaly_detection"):
        income = st.number_input("Income", min_value=0)
        age = st.number_input("Age", min_value=0)
        dependents = st.number_input("Dependents", min_value=0)
        occupation = st.text_input("Occupation")
        city_tier = st.number_input("City Tier", min_value=1, max_value=3)

        rent = st.number_input("Rent", min_value=0)
        loan_repayment = st.number_input("Loan Repayment", min_value=0)
        insurance = st.number_input("Insurance", min_value=0)
        groceries = st.number_input("Groceries", min_value=0)
        transport = st.number_input("Transport", min_value=0)
        eating_out = st.number_input("Eating Out", min_value=0)
        entertainment = st.number_input("Entertainment", min_value=0)
        utilities = st.number_input("Utilities", min_value=0)
        healthcare = st.number_input("Healthcare", min_value=0)
        education = st.number_input("Education", min_value=0)
        miscellaneous = st.number_input("Miscellaneous", min_value=0)

        savings = st.number_input("Desired Savings Percentage", min_value=0, max_value=100)

        submit = st.form_submit_button("Check for Anomalies")

    if submit:
        st.write("🔄 Submitting for anomaly detection...")
        payload = {
            "Income": income,
            "Age": age,
            "Dependents": dependents,
            "Occupation": occupation,
            "City_Tier": city_tier,
            "Rent": rent,
            "Loan_Repayment": loan_repayment,
            "Insurance": insurance,
            "Groceries": groceries,
            "Transport": transport,
            "Eating_Out": eating_out,
            "Entertainment": entertainment,
            "Utilities": utilities,
            "Healthcare": healthcare,
            "Education": education,
            "Miscellaneous": miscellaneous,
            "Desired_Savings_Percentage": savings
        }

        response = send_request("predict/anomaly", payload)

        if response is not None:
            st.success("✅ Anomaly detection completed!")

            result = response.get("Anomaly_Detection", None)

            st.write("### 📊 Anomaly Detection Result")
            
            if result is True:
                st.warning("⚠️ Anomaly detected in your financial pattern!")
            elif result is False:
                st.info("✅ Everything looks normal. No anomalies detected.")
            else:
                st.error("❌ Could not interpret the response.")
        else:
            st.error("❌ Failed to get anomaly detection result.")
def savings_efficiency_form():
    st.subheader("💰 Savings Efficiency")

    with st.form("savings_efficiency"):
        income = st.number_input("Income", min_value=0)
        age = st.number_input("Age", min_value=0)
        dependents = st.number_input("Dependents", min_value=0)
        occupation = st.text_input("Occupation")
        city_tier = st.selectbox("City Tier", [1, 2, 3])
        rent = st.number_input("Rent", min_value=0.0)
        loan_repayment = st.number_input("Loan Repayment", min_value=0.0)
        insurance = st.number_input("Insurance", min_value=0.0)
        groceries = st.number_input("Groceries", min_value=0.0)
        transport = st.number_input("Transport", min_value=0.0)
        eating_out = st.number_input("Eating Out", min_value=0.0)
        entertainment = st.number_input("Entertainment", min_value=0.0)
        utilities = st.number_input("Utilities", min_value=0.0)
        healthcare = st.number_input("Healthcare", min_value=0.0)
        education = st.number_input("Education", min_value=0.0)
        miscellaneous = st.number_input("Miscellaneous", min_value=0.0)
        desired_savings_percentage = st.number_input("Desired Savings Percentage", min_value=0.0, max_value=100.0)

        submit = st.form_submit_button("Check Savings Efficiency")

    if submit:
        st.write("🔄 Submitting for savings efficiency analysis...")
        payload = {
            "Income": income,
            "Age": age,
            "Dependents": dependents,
            "Occupation": occupation,
            "City_Tier": city_tier,
            "Rent": rent,
            "Loan_Repayment": loan_repayment,
            "Insurance": insurance,
            "Groceries": groceries,
            "Transport": transport,
            "Eating_Out": eating_out,
            "Entertainment": entertainment,
            "Utilities": utilities,
            "Healthcare": healthcare,
            "Education": education,
            "Miscellaneous": miscellaneous,
            "Desired_Savings_Percentage": desired_savings_percentage
        }

        response = send_request("predict/savings", payload)

        if response is not None:
            st.success("✅ Savings Efficiency Analysis Successful!")
            st.write("### 📋 Savings Insight")

            if isinstance(response, dict):
                for key, value in response.items():
                    st.markdown(f"- **{key.replace('_', ' ')}**: {value}")
            else:
                st.warning("⚠️ Unexpected response format.")
        else:
            st.error("❌ Failed to fetch savings efficiency.")

def financial_score_form():
    st.subheader("📊 Financial Score")

    with st.form("financial_score"):
        income = st.number_input("Income", min_value=0)
        age = st.number_input("Age", min_value=0)
        dependents = st.number_input("Dependents", min_value=0)
        occupation = st.text_input("Occupation")
        city_tier = st.selectbox("City Tier", [1, 2, 3])
        rent = st.number_input("Rent", min_value=0.0)
        loan_repayment = st.number_input("Loan Repayment", min_value=0.0)
        insurance = st.number_input("Insurance", min_value=0.0)
        groceries = st.number_input("Groceries", min_value=0.0)
        transport = st.number_input("Transport", min_value=0.0)
        eating_out = st.number_input("Eating Out", min_value=0.0)
        entertainment = st.number_input("Entertainment", min_value=0.0)
        utilities = st.number_input("Utilities", min_value=0.0)
        healthcare = st.number_input("Healthcare", min_value=0.0)
        education = st.number_input("Education", min_value=0.0)
        miscellaneous = st.number_input("Miscellaneous", min_value=0.0)
        desired_savings_percentage = st.number_input("Desired Savings Percentage", min_value=0.0, max_value=100.0)
        
        submit = st.form_submit_button("Check Financial Score")

    if submit:
        st.write("🔄 Submitting for financial score analysis...")
        payload = {
            "Income": income,
            "Age": age,
            "Dependents": dependents,
            "Occupation": occupation,
            "City_Tier": city_tier,
            "Rent": rent,
            "Loan_Repayment": loan_repayment,
            "Insurance": insurance,
            "Groceries": groceries,
            "Transport": transport,
            "Eating_Out": eating_out,
            "Entertainment": entertainment,
            "Utilities": utilities,
            "Healthcare": healthcare,
            "Education": education,
            "Miscellaneous": miscellaneous,
            "Desired_Savings_Percentage": desired_savings_percentage
        }

        response = send_request("predict/score", payload)

        if response is not None:
            st.success("✅ Financial score retrieved successfully!")
            st.write("### 🧮 Your Financial Health Report")

            if isinstance(response, dict):
                for key, value in response.items():
                    st.markdown(f"- **{key.replace('_', ' ')}**: {value}")
            else:
                st.warning("⚠️ Unexpected response format.")
        else:
            st.error("❌ Failed to fetch financial score.")

def personalized_recommendation_form():
    st.subheader("💡 Personalized Financial Recommendations")
    
    with st.form("personalized_recommendation"):
        income = st.number_input("Income", min_value=0)
        age = st.number_input("Age", min_value=0)
        dependents = st.number_input("Dependents", min_value=0)
        occupation = st.text_input("Occupation")
        city_tier = st.selectbox("City Tier", [1, 2, 3])
        rent = st.number_input("Rent", min_value=0.0)
        loan_repayment = st.number_input("Loan Repayment", min_value=0.0)
        insurance = st.number_input("Insurance", min_value=0.0)
        groceries = st.number_input("Groceries", min_value=0.0)
        transport = st.number_input("Transport", min_value=0.0)
        eating_out = st.number_input("Eating Out", min_value=0.0)
        entertainment = st.number_input("Entertainment", min_value=0.0)
        utilities = st.number_input("Utilities", min_value=0.0)
        healthcare = st.number_input("Healthcare", min_value=0.0)
        education = st.number_input("Education", min_value=0.0)
        miscellaneous = st.number_input("Miscellaneous", min_value=0.0)
        desired_savings_percentage = st.number_input("Desired Savings Percentage", min_value=0.0, max_value=100.0)

        submit = st.form_submit_button("Get Recommendations")

    if submit:
        st.write("🔄 Submitting for personalized recommendations...")
        payload = {
            "Income": income,
            "Age": age,
            "Dependents": dependents,
            "Occupation": occupation,
            "City_Tier": city_tier,
            "Rent": rent,
            "Loan_Repayment": loan_repayment,
            "Insurance": insurance,
            "Groceries": groceries,
            "Transport": transport,
            "Eating_Out": eating_out,
            "Entertainment": entertainment,
            "Utilities": utilities,
            "Healthcare": healthcare,
            "Education": education,
            "Miscellaneous": miscellaneous,
            "Desired_Savings_Percentage": desired_savings_percentage
        }

        response = send_request("predict/recommendation", payload)

        if response is not None:
            st.success("✅ Recommendations fetched successfully!")
            st.write("### 🧾 Your Personalized Recommendations")

            if isinstance(response, dict):
                for key, value in response.items():
                    st.markdown(f"- **{key.replace('_', ' ')}**: {value}")
            else:
                st.info("ℹ️ No specific recommendations returned.")
        else:
            st.error("❌ Failed to get recommendations.")






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