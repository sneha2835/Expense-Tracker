import streamlit as st
import requests
import json
from datetime import date, datetime
import uuid
import time
import pandas as pd

# Initialize session state for form keys
if 'form_keys' not in st.session_state:
    st.session_state.form_keys = {
        'login': str(time.time()),
        'register': str(time.time() + 1),
        'profile': str(time.time() + 2),
        'budget': str(time.time() + 3),
        'transaction': str(time.time() + 4),
        'ai': str(time.time() + 5)
    }

# This MUST be the first Streamlit command
st.set_page_config(
    page_title="Finalyze - Personal Finance Tracker",
    page_icon="💸",
    layout="wide"
)

# Constants
BASE_URL = "http://127.0.0.1:8000/api"

# Session state initialization
if "access_token" not in st.session_state:
    st.session_state.access_token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "active_section" not in st.session_state:
    st.session_state.active_section = "dashboard"
if "active_subsection" not in st.session_state:
    st.session_state.active_subsection = None

# Theme configuration
def set_theme():
    st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: #f8f9fa;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 8px 16px;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
        }
        .stNumberInput>div>div>input {
            border-radius: 8px;
        }
        .stSelectbox>div>div>select {
            border-radius: 8px;
        }
        .stDateInput>div>div>input {
            border-radius: 8px;
        }
        .stTimeInput>div>div>input {
            border-radius: 8px;
        }
        .css-1aumxhk {
            background-color: #f0f2f6;
            border-radius: 8px;
            padding: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

def save_token(token):
    st.session_state.access_token = token

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.access_token}"} if st.session_state.access_token else {}

# Authentication Functions
def login_user():
    """User login using JWT with unique form keys"""
    st.subheader("🔑 Login")
    
    # Generate new form key if none exists
    if 'login_form_key' not in st.session_state:
        st.session_state.login_form_key = f"login_form_{time.time()}"
    
    with st.form(key=st.session_state.login_form_key):
        email = st.text_input("Email", key=f"email_{st.session_state.login_form_key}")
        password = st.text_input("Password", type="password", key=f"password_{st.session_state.login_form_key}")
        
        if st.form_submit_button("Login"):
            payload = {"email": email, "password": password}
            response = requests.post(f"{BASE_URL}/auth/login/", json=payload)

            if response.status_code == 200:
                data = response.json()
                save_token(data["access"])
                st.session_state.user_email = email
                st.session_state.active_section = "dashboard"
                # Invalidate current form key
                del st.session_state.login_form_key
                st.success("Login successful!")
                st.rerun()
            else:
                # Invalidate current form key on failure
                del st.session_state.login_form_key
                st.error(f"Login failed: {response.text}")
                st.rerun()

def register_user():
    """User registration with unique form keys"""
    st.subheader("📝 Register")
    
    if 'register_form_key' not in st.session_state:
        st.session_state.register_form_key = f"register_form_{time.time()}"
    
    with st.form(key=st.session_state.register_form_key):
        username = st.text_input("Username", key=f"username_{st.session_state.register_form_key}")
        email = st.text_input("Email", key=f"email_{st.session_state.register_form_key}")
        password = st.text_input("Password", type="password", key=f"password_{st.session_state.register_form_key}")
        confirm_password = st.text_input("Confirm Password", type="password", key=f"confirm_{st.session_state.register_form_key}")

        if st.form_submit_button("Register"):
            if password != confirm_password:
                del st.session_state.register_form_key
                st.error("Passwords do not match!")
                st.rerun()
                return

            payload = {"username": username, "email": email, "password": password}
            response = requests.post(f"{BASE_URL}/auth/register/", json=payload)

            if response.status_code == 201:
                st.success("Registration successful! Please log in.")
            else:
                st.error(f"Registration failed: {response.json()}")
            # Invalidate current form key
            del st.session_state.register_form_key
            st.rerun()

def logout():
    """Log out user"""
    st.session_state.access_token = None
    st.session_state.user_email = ""
    st.session_state.active_section = None
    st.session_state.active_subsection = None
    st.success("Logged out successfully!")
    
### ✅ Navigation & Main App
def sidebar_navigation():
    """Render the sidebar navigation with unique keys"""
    with st.sidebar:
        st.image(r"C:\Users\sneha\OneDrive\Pictures\Screenshots\Screenshot 2025-04-15 034634.png", width=150)
        st.write(f"Logged in as: {st.session_state.user_email}")
        
        st.markdown("## Navigation")
        if st.button("📊 Dashboard", key="sidebar_dashboard_btn"):
            st.session_state.active_section = "dashboard"
            st.session_state.active_subsection = None
            st.rerun()
        
        if st.button("👤 Profile", key="sidebar_profile_btn"):
            st.session_state.active_section = "profile"
            st.session_state.active_subsection = None
            st.rerun()
        
        if st.button("💰 Budget", key="sidebar_budget_btn"):
            st.session_state.active_section = "budget"
            st.session_state.active_subsection = None
            st.rerun()
        
        if st.button("💳 Transactions", key="sidebar_transactions_btn"):
            st.session_state.active_section = "transactions"
            st.session_state.active_subsection = None
            st.rerun()
        
        if st.button("🤖 AI Tools", key="sidebar_ai_btn"):
            st.session_state.active_section = "ai"
            st.session_state.active_subsection = None
            st.rerun()
        
        st.markdown("---")
        if st.button("🚪 Logout", key="sidebar_logout_btn"):
            logout()
            st.rerun()


# User Profile Functions
def create_user_profile():
    """Create a new user profile with unique form key"""
    st.subheader("➕ Create Profile")
    
    if 'create_profile_key' not in st.session_state:
        st.session_state.create_profile_key = f"create_profile_{time.time()}"
    
    with st.form(key=st.session_state.create_profile_key):
        full_name = st.text_input("Full Name", key=f"name_{st.session_state.create_profile_key}")
        email = st.text_input("Email", key=f"email_{st.session_state.create_profile_key}")
        

        if st.form_submit_button("Submit Profile"):
            payload = {"full_name": full_name, "email": email}
            
            if response.status_code == 201:
                st.success("✅ Profile created successfully!")
                del st.session_state.create_profile_key
                st.session_state.active_subsection = None
                st.rerun()
            else:
                del st.session_state.create_profile_key
                st.error(f"❌ Failed to create profile: {response.text}")
                st.rerun()

def view_user_profile():
    """View user profile with styled layout"""
    st.subheader("👤 View Profile")
    response = requests.get(f"{BASE_URL}/dashboard/profile/", headers=get_headers())
    
    if response.status_code == 200:
        data = response.json()

        col1, col2 = st.columns([1, 2])
        with col1:
            profile_pic_url = data.get("profile_picture")
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

        if st.button("✏️ Edit Profile"):
            st.session_state.active_subsection = "update_profile"
            st.rerun()

    elif response.status_code == 404:
        st.warning("No profile found. Please create one first.")
    else:
        st.error("Failed to fetch profile.")

def update_user_profile():
    """Update existing user profile with unique form key"""
    st.subheader("✏️ Update Profile")
    response = requests.get(f"{BASE_URL}/dashboard/profile/", headers=get_headers())
    if response.status_code != 200:
        st.error("Failed to load current profile.")
        return

    data = response.json()
    
    if 'update_profile_key' not in st.session_state:
        st.session_state.update_profile_key = f"update_profile_{time.time()}"
    
    with st.form(key=st.session_state.update_profile_key):
        full_name = st.text_input("Full Name", 
                                value=data.get("full_name", ""),
                                key=f"name_{st.session_state.update_profile_key}")
        email = st.text_input("Email", 
                            value=data.get("email", ""),
                            key=f"email_{st.session_state.update_profile_key}")
        profile_picture = st.file_uploader("Upload New Profile Picture", 
                                         type=["jpg", "png"],
                                         key=f"upload_{st.session_state.update_profile_key}")

        if st.form_submit_button("Update Profile"):
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
                del st.session_state.update_profile_key
                st.session_state.active_subsection = None
                st.rerun()
            else:
                del st.session_state.update_profile_key
                st.error(f"❌ Update failed: {response.text}")
                st.rerun()

def delete_user_profile():
    """Delete user profile with unique form key"""
    st.subheader("🗑️ Delete Profile")
    st.warning("This action cannot be undone!")
    
    if 'delete_profile_key' not in st.session_state:
        st.session_state.delete_profile_key = f"delete_profile_{time.time()}"
    
    with st.form(key=st.session_state.delete_profile_key):
        confirm = st.checkbox("I understand this will permanently delete my profile",
                             key=f"confirm_{st.session_state.delete_profile_key}")
        if confirm and st.form_submit_button("Delete Profile"):
            response = requests.delete(f"{BASE_URL}/dashboard/profile/delete/", headers=get_headers())

            if response.status_code == 204:
                st.success("🧹 Profile deleted successfully!")
                del st.session_state.delete_profile_key
                st.session_state.active_subsection = None
                st.rerun()
            else:
                del st.session_state.delete_profile_key
                st.error(f"❌ Deletion failed: {response.text}")
                st.rerun()

### ✅ Navigation & Main App


# [Rest of your functions... (budget, transactions, AI views etc.)]
# Implement all other functions following the same pattern with unique form keys

### ✅ Budget Functions
def enter_budget():
    """Enter new budget"""
    st.subheader("📊 Enter Budget")
    with st.form("enter_budget_form"):
        income = st.number_input("Income")
        savings_goal = st.number_input("Savings Goal")
        month = st.date_input("Budget Month", value=date.today())
        budget_limit = st.number_input("Budget Limit")
        category = st.text_input("Category")

        if st.form_submit_button("Submit Budget"):
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
                st.session_state.budget_id = budget["id"]
                st.success("✅ Budget created successfully!")
                st.session_state.active_subsection = None
            else:
                st.error(f"🚫 Error saving budget: {response.text}")

def update_budget():
    """Update existing budget"""
    st.subheader("🔄 Update Budget")
    budget_id = st.text_input("Enter Budget ID to update")
    
    if budget_id:
        response = requests.get(f"{BASE_URL}/finance/budget/{budget_id}/", headers=get_headers())
        if response.status_code == 200:
            current_data = response.json()
            
            # Convert string values to float for number_input
            try:
                current_income = float(current_data.get("income", 0))
                current_savings = float(current_data.get("savings_goal", 0))
                current_limit = float(current_data.get("budget_limit", 0))
            except (ValueError, TypeError):
                st.error("Invalid number format in budget data")
                return
            
            with st.form("update_budget_form"):
                income = st.number_input(
                    "New Income", 
                    value=current_income,
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f"
                )
                savings_goal = st.number_input(
                    "New Savings Goal", 
                    value=current_savings,
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f"
                )
                budget_limit = st.number_input(
                    "New Budget Limit", 
                    value=current_limit,
                    min_value=0.0,
                    step=1000.0,
                    format="%.2f"
                )
                category = st.text_input(
                    "New Category", 
                    value=current_data.get("category", "")
                )
                month = st.date_input(
                    "New Budget Month", 
                    value=datetime.strptime(
                        current_data.get("month", str(date.today())), 
                        "%Y-%m-%d"
                    ).date()
                )

                if st.form_submit_button("Update Budget"):
                    payload = {
                        "income": str(income),  # Convert back to string for API
                        "savings_goal": str(savings_goal),
                        "month": month.strftime("%Y-%m-%d"),
                        "budget_limit": str(budget_limit),
                        "category": category,
                    }
                    response = requests.put(
                        f"{BASE_URL}/finance/budget/{budget_id}/", 
                        headers=get_headers(), 
                        json=payload
                    )
                    if response.status_code in [200, 202]:
                        st.success("✅ Budget updated successfully!")
                        st.session_state.active_subsection = None
                        st.rerun()
                    else:
                        st.error(f"Error updating budget: {response.text}")
                        st.json(response.json())  # Show detailed error
        else:
            st.error(f"Budget not found (Status: {response.status_code})")
            if response.status_code != 404:
                st.json(response.json())  # Show error details if available

def view_budget():
    """View existing budgets"""
    st.subheader("💼 View Budgets")
    response = requests.get(f"{BASE_URL}/finance/budget/", headers=get_headers())

    if response.status_code == 200:
        budgets = response.json()

        if not budgets:
            st.warning("You don't have any budgets yet.")
        else:
            for budget in budgets:
                with st.expander(f"Budget ID: {budget['id']} - {budget['category']}"):
                    st.markdown(f"""
                        <div style="background-color:#ffffff; color:#000000; padding:20px; 
                                    border-radius:12px; border:1px solid #dcdcdc; 
                                    box-shadow: 0 2px 6px rgba(0,0,0,0.05); font-family:Arial, sans-serif;">
                            <p><strong>💰 Income:</strong> ₹{float(budget['income']):,.2f}</p>
                            <p><strong>🎯 Savings Goal:</strong> ₹{float(budget['savings_goal']):,.2f}</p>
                            <p><strong>🧾 Budget Limit:</strong> ₹{float(budget['budget_limit']):,.2f}</p>
                            <p><strong>🏷️ Category:</strong> {budget['category'].capitalize()}</p>
                            <p><strong>🗓️ Month:</strong> {budget['month']}</p>
                            <p><strong>🕒 Created At:</strong> {datetime.strptime(budget['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%b %d, %Y %I:%M %p")}</p>
                        </div>
                    """, unsafe_allow_html=True)

    elif response.status_code == 401:
        st.error("❌ Unauthorized: Please check your token or login again.")
    else:
        st.error(f"❌ Something went wrong: {response.status_code} - {response.text}")

def delete_budget():
    """Delete a budget with confirmation and debug information"""
    st.subheader("🗑️ Delete Budget")
    
    # Get budget ID from user
    budget_id = st.text_input("Enter Budget ID to delete")
    
    if budget_id:
        try:
            # First verify the budget exists
            headers = get_headers()
            verify_url = f"{BASE_URL}/finance/budget/{budget_id}/"
            
            with st.spinner("Checking budget..."):
                verify_response = requests.get(verify_url, headers=headers)
            
            if verify_response.status_code == 200:
                budget = verify_response.json()
                
                # Show budget details for confirmation
                st.warning(f"""
                **You're about to delete:**
                - Month: {budget['month']}
                - Category: {budget['category']}
                - Income: ₹{float(budget['income']):,.2f}
                """)
                
                # Double confirmation
                if st.checkbox("I understand this cannot be undone", key=f"confirm_del_{budget_id}"):
                    if st.button("Permanently Delete Budget", type="primary"):
                        with st.spinner("Deleting..."):
                            del_response = requests.delete(verify_url, headers=headers)
                        
                        if del_response.status_code == 204:
                            st.success("✅ Budget deleted successfully!")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(f"""
                            ❌ Deletion failed (Status {del_response.status_code})
                            Response: {del_response.text}
                            """)
                            st.json(del_response.json())  # Show full error response
                
            elif verify_response.status_code == 404:
                st.error("❌ Budget not found. Please check the ID.")
            else:
                st.error(f"Verification failed (Status {verify_response.status_code})")
                st.json(verify_response.json())  # Show error details

        except requests.exceptions.RequestException as e:
            st.error(f"""
            ❌ Network error occurred:
            {str(e)}
            """)
            st.write("Please check your connection and try again")

        except Exception as e:
            st.error(f"""
            ❌ Unexpected error:
            {str(e)}
            """)
            st.write("Please check the console for details")

### ✅ Transaction Functions
def log_transaction():
    """Log a new transaction"""
    st.subheader("💳 Log Transaction")
    with st.form("log_transaction_form"):
        amount = st.number_input("Amount", min_value=0.0)
        
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

        if st.form_submit_button("Submit Transaction"):
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
                st.success("✅ Transaction added successfully!")
            else:
                st.error(f"Failed to log transaction: {response.json()}")

def recurring_transaction():
    """Log a recurring transaction"""
    st.subheader("🔄 Recurring Transaction")
    with st.form("recurring_transaction_form"):
        amount = st.number_input("Amount", min_value=0.0)
        
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

        if st.form_submit_button("Submit Recurring Transaction"):
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
                st.success("✅ Recurring transaction saved successfully!")
            else:
                st.error(f"Failed to save recurring transaction: {response.json()}")

def list_transactions():
    """List all transactions with proper columns and action buttons"""
    st.subheader("📜 Transaction History")
    response = requests.get(f"{BASE_URL}/finance/transactions/", headers=get_headers())
    recurring_response = requests.get(f"{BASE_URL}/finance/recurring-transactions/", headers=get_headers())

    if response.status_code == 200 and recurring_response.status_code == 200:
        transactions = response.json()
        recurring_transactions = recurring_response.json()

        if transactions or recurring_transactions:
            # Regular Transactions
            st.write("### Regular Transactions")
            if transactions:
                # Create a DataFrame with proper column names
                regular_df = pd.DataFrame([{
                    "ID": txn["id"],
                    "Date": txn["transaction_date"],
                    "Time": txn.get("transaction_time", ""),
                    "Amount (₹)": float(txn["amount"]),
                    "Category": txn["category"],
                    "Payment Method": txn["payment_method"],
                    "Merchant": txn.get("merchant_name", ""),
                    "Description": txn.get("transaction_description", "")
                } for txn in transactions])
                
                # Format the DataFrame display
                formatted_df = regular_df.copy()
                formatted_df["Amount (₹)"] = formatted_df["Amount (₹)"].apply(lambda x: f"₹{x:,.2f}")
                
                # Display the formatted table
                st.dataframe(
                    formatted_df,
                    column_config={
                        "ID": st.column_config.NumberColumn("ID"),
                        "Date": st.column_config.DateColumn("Date"),
                        "Time": st.column_config.TimeColumn("Time"),
                        "Amount (₹)": st.column_config.NumberColumn("Amount"),
                        "Category": "Category",
                        "Payment Method": "Payment Method",
                        "Merchant": "Merchant",
                        "Description": "Description"
                    },
                    hide_index=True,
                    use_container_width=True
                )
                              
            # Recurring Transactions
            st.write("### Recurring Transactions")
            if recurring_transactions:
                recurring_df = pd.DataFrame([{
                    "ID": r_txn["id"],
                    "Start Date": r_txn["start_date"],
                    "Amount (₹)": float(r_txn["amount"]),
                    "Category": r_txn["category"],
                    "Frequency": r_txn["frequency"],
                    "Next Due": r_txn["next_due_date"],
                    "Description": r_txn.get("description", "")
                } for r_txn in recurring_transactions])
                
                st.dataframe(
                    recurring_df,
                    column_config={
                        "ID": st.column_config.NumberColumn("ID"),
                        "Start Date": st.column_config.DateColumn("Start Date"),
                        "Amount (₹)": st.column_config.NumberColumn("Amount"),
                        "Category": "Category",
                        "Frequency": "Frequency",
                        "Next Due": st.column_config.DateColumn("Next Due"),
                        "Description": "Description"
                    },
                    hide_index=True,
                    use_container_width=True
                )
            else:
                st.info("No recurring transactions found.")
        else:
            st.info("No transactions found.")
    else:
        st.error("❌ Failed to fetch transactions.")

def update_transaction():
    """Update an existing transaction"""
    st.subheader("🔄 Update Transaction")
    transaction_id = st.text_input("Enter Transaction ID to update")
    
    if transaction_id:
        # Get current transaction data
        response = requests.get(
            f"{BASE_URL}/finance/transactions/{transaction_id}/", 
            headers=get_headers()
        )
        
        if response.status_code == 200:
            current_data = response.json()
            
            with st.form("update_transaction_form"):
                amount = st.number_input(
                    "Amount", 
                    value=float(current_data.get("amount", 0)),
                    min_value=0.0,
                    step=0.01,
                    format="%.2f"
                )
                
                categories = [
                    "Rent", "Loan_Repayment", "Insurance", "Groceries", "Transport", 
                    "Eating_Out", "Entertainment", "Utilities", "Healthcare", 
                    "Education", "Miscellaneous"
                ]
                category = st.selectbox(
                    "Category", 
                    categories,
                    index=categories.index(current_data.get("category", "Miscellaneous"))
                )
                
                transaction_date = st.date_input(
                    "Transaction Date",
                    value=datetime.strptime(
                        current_data.get("transaction_date", str(date.today())), 
                        "%Y-%m-%d"
                    ).date()
                )
                
                transaction_time = st.time_input(
                    "Transaction Time",
                    value=datetime.strptime(
                        current_data.get("transaction_time", "12:00:00"), 
                        "%H:%M:%S"
                    ).time()
                )
                
                merchant_name = st.text_input(
                    "Merchant Name", 
                    value=current_data.get("merchant_name", "")
                )
                
                payment_method = st.selectbox(
                    "Payment Method", 
                    ["Cash", "UPI", "Card", "Net Banking"],
                    index=["Cash", "UPI", "Card", "Net Banking"].index(
                        current_data.get("payment_method", "Cash"))
                )
                
                transaction_description = st.text_input(
                    "Description", 
                    value=current_data.get("transaction_description", "")
                )

                if st.form_submit_button("Update Transaction"):
                    payload = {
                        "amount": str(amount),
                        "category": category,
                        "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                        "transaction_time": transaction_time.strftime("%H:%M"),
                        "merchant_name": merchant_name,
                        "payment_method": payment_method,
                        "transaction_description": transaction_description
                    }
                    
                    response = requests.put(
                        f"{BASE_URL}/finance/transactions/{transaction_id}/", 
                        headers=get_headers(), 
                        json=payload
                    )
                    
                    if response.status_code == 200:
                        st.success("✅ Transaction updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Error updating transaction: {response.text}")

        elif response.status_code == 404:
            st.error("Transaction not found")
        else:
            st.error(f"Error fetching transaction: {response.status_code}")

def delete_transaction():
    """Delete a transaction"""
    st.subheader("🗑️ Delete Transaction")
    transaction_id = st.text_input("Enter Transaction ID to delete")
    
    if transaction_id:
        # First show transaction details
        response = requests.get(
            f"{BASE_URL}/finance/transactions/{transaction_id}/", 
            headers=get_headers()
        )
        
        if response.status_code == 200:
            transaction = response.json()
            
            st.warning(f"""
            **You're about to delete:**
            - Amount: ₹{float(transaction['amount']):,.2f}
            - Category: {transaction['category']}
            - Date: {transaction['transaction_date']} at {transaction['transaction_time']}
            - Merchant: {transaction.get('merchant_name', 'N/A')}
            """)
            
            if st.checkbox("I confirm I want to delete this transaction"):
                if st.button("Permanently Delete", type="primary"):
                    response = requests.delete(
                        f"{BASE_URL}/finance/transactions/{transaction_id}/", 
                        headers=get_headers()
                    )
                    
                    if response.status_code == 204:
                        st.success("✅ Transaction deleted successfully!")
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error(f"Error deleting transaction: {response.text}")
        
        elif response.status_code == 404:
            st.error("Transaction not found")
        else:
            st.error(f"Error fetching transaction: {response.status_code}")

def download_reports():
    """Download transaction reports"""
    st.subheader("📥 Download Reports")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Download CSV Report"):
            csv_response = requests.get(f"{BASE_URL}/export/csv/", headers=get_headers())
            if csv_response.status_code == 200:
                st.download_button(
                    label="Click to download",
                    data=csv_response.content,
                    file_name="transactions.csv",
                    mime="text/csv"
                )
            else:
                st.error("Failed to download CSV report.")
    
    with col2:
        if st.button("Download PDF Report"):
            pdf_response = requests.get(f"{BASE_URL}/export/pdf/", headers=get_headers())
            if pdf_response.status_code == 200:
                st.download_button(
                    label="Click to download",
                    data=pdf_response.content,
                    file_name="transactions.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to download PDF report.")

### ✅ AI Prediction Functions
def send_request(endpoint, payload):
    """Helper function to send API requests"""
    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}",
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/predict/{endpoint}/"

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            st.write("Response Text:", response.text)
            return None
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

def expense_prediction():
    """Expense prediction form"""
    st.subheader("📊 Expense Prediction")
    
    with st.form("expense_prediction_form"):
        # Basic Information
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        # Essential Expenses
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        # Lifestyle Expenses
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        # Other Expenses
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Predict Expense Breakdown"):
            payload = {
                "Income": income, "Age": age, "Dependents": dependents, "Occupation": occupation,
                "City_Tier": city_tier, "Rent": rent, "Loan_Repayment": loan_repayment,
                "Insurance": insurance, "Groceries": groceries, "Transport": transport,
                "Eating_Out": eating_out, "Entertainment": entertainment, "Utilities": utilities,
                "Healthcare": healthcare, "Education": education, "Miscellaneous": miscellaneous,
                "Desired_Savings_Percentage": savings
            }

            response = send_request("expense", payload)

            if response:
                st.success("✅ Prediction successful!")
                prediction = response.get("Expense_Prediction", {})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Disposable Income", f"₹{prediction.get('Disposable_Income', 0):,.2f}")
                    st.metric("Total Expenses", f"₹{prediction.get('Total_Expenses', 0):,.2f}")
                with col2:
                    st.write("### Category Breakdown")
                    for category, amount in prediction.get("Category_Expenses", {}).items():
                        st.markdown(f"- **{category}:** ₹{amount:,.2f}")
            else:
                st.error("❌ Failed to get prediction.")

def overspending_alert():
    """Overspending alert form"""
    st.subheader("🚨 Overspending Alert")
    
    with st.form("overspending_alert_form"):
        # Basic Information
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        # Essential Expenses
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        # Lifestyle Expenses
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        # Other Expenses
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Check Overspending Risk"):
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

            response = send_request("overspending", payload)

            if response:
                st.success("✅ Analysis completed!")
                alert = response.get("Overspending_Alert", None)
                
                if alert is True:
                    st.error("⚠️ Overspending Detected!")
                    st.markdown("""
                    ### Recommendations:
                    - Review your discretionary spending (eating out, entertainment)
                    - Consider reducing expenses in high-spend categories
                    - Set up spending alerts for better monitoring
                    """)
                else:
                    st.success("🎉 Your spending is within healthy limits!")
            else:
                st.error("❌ Failed to analyze spending.")

def anomaly_detection():
    """Anomaly detection form"""
    st.subheader("🔍 Anomaly Detection")
    
    with st.form("anomaly_detection_form"):
        # Basic Information
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        # Essential Expenses
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        # Lifestyle Expenses
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        # Other Expenses
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Check for Anomalies"):
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

            response = send_request("anomaly", payload)

            if response:
                st.success("✅ Analysis completed!")
                anomaly = response.get("Anomaly_Detection", False)
                
                if anomaly:
                    st.error("⚠️ Anomaly Detected in your spending patterns!")
                    st.markdown("""
                    ### Suggested Actions:
                    - Review recent large transactions
                    - Verify recurring payments
                    - Check for unauthorized transactions
                    - Set up transaction alerts
                    """)
                else:
                    st.success("✅ No anomalies detected in your spending patterns")
            else:
                st.error("❌ Failed to detect anomalies.")

def financial_score():
    """Financial score form"""
    st.subheader("📊 Financial Score")
    
    with st.form("financial_score_form"):
        # Basic Information
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        # Essential Expenses
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        # Lifestyle Expenses
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        # Other Expenses
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Calculate Financial Score"):
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

            response = send_request("score", payload)

            if response:
                st.success("✅ Score calculated successfully!")
                score = response.get("Financial_Health_Score", 0)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Your Financial Health Score", f"{score:.1f}/100")
                    if score >= 75:
                        st.success("Excellent financial health!")
                    elif score >= 50:
                        st.warning("Moderate financial health - room for improvement")
                    else:
                        st.error("Poor financial health - needs attention")
                
                with col2:
                    st.write("### Improvement Tips")
                    st.markdown("""
                    - Increase your savings rate
                    - Reduce high-interest debt
                    - Review discretionary spending
                    - Consider additional income streams
                    """)
            else:
                st.error("❌ Failed to calculate score.")

def personalized_recommendations():
    """Personalized recommendations form"""
    st.subheader("💡 Personalized Recommendations")
    
    with st.form("personalized_recommendation_form"):
        # Basic Information
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        # Essential Expenses
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        # Lifestyle Expenses
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        # Other Expenses
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Get Recommendations"):
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

            response = send_request("recommendation", payload)

            if response:
                st.success("✅ Recommendations generated successfully!")
                recommendations = response.get("Personalized_Recommendations", {})
                
                if recommendations:
                    st.write("### 💰 Your Personalized Budget Recommendations")
                    cols = st.columns(2)
                    with cols[0]:
                        st.metric("Recommended Rent", f"₹{recommendations.get('Rent', 0):,.2f}")
                        st.metric("Recommended Groceries", f"₹{recommendations.get('Groceries', 0):,.2f}")
                    with cols[1]:
                        st.metric("Recommended Savings", f"₹{recommendations.get('Savings', 0):,.2f}")
                        st.metric("Discretionary Spending", f"₹{recommendations.get('Discretionary', 0):,.2f}")
                else:
                    st.info("No specific recommendations available based on your input.")
            else:
                st.error("❌ Failed to get recommendations.")
           
def savings_efficiency():
    """Savings efficiency analysis form"""
    st.subheader("💰 Savings Efficiency")
    
    with st.form("savings_efficiency_form"):
        # Basic Information
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)
        with col1:
            income = st.number_input("Monthly Income (₹)", min_value=0, value=50000)
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            dependents = st.number_input("Number of Dependents", min_value=0, value=0)
        with col2:
            occupation = st.selectbox("Occupation", ["Salaried", "Business", "Professional", "Retired", "Student", "Other"])
            city_tier = st.selectbox("City Tier", [1, 2, 3], index=1)
            savings = st.number_input("Desired Savings (%)", min_value=0, max_value=100, value=20)
        
        # Essential Expenses
        st.markdown("### Essential Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            rent = st.number_input("Rent/Mortgage", min_value=0, value=15000)
            groceries = st.number_input("Groceries", min_value=0, value=8000)
            transport = st.number_input("Transport", min_value=0, value=3000)
        with col2:
            loan_repayment = st.number_input("Loan Repayment", min_value=0, value=5000)
            insurance = st.number_input("Insurance", min_value=0, value=2000)
            utilities = st.number_input("Utilities", min_value=0, value=2000)
        
        # Lifestyle Expenses
        st.markdown("### Lifestyle Expenses (₹)")
        col1, col2 = st.columns(2)
        with col1:
            eating_out = st.number_input("Dining Out", min_value=0, value=4000)
            entertainment = st.number_input("Entertainment", min_value=0, value=3000)
        with col2:
            healthcare = st.number_input("Healthcare", min_value=0, value=2000)
            education = st.number_input("Education", min_value=0, value=3000)
        
        # Other Expenses
        st.markdown("### Other Expenses (₹)")
        miscellaneous = st.number_input("Miscellaneous", min_value=0, value=2000)
        
        if st.form_submit_button("Analyze Savings Efficiency"):
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

            response = send_request("savings", payload)

            if response:
                st.success("✅ Savings analysis completed!")
                result = response.get("Savings_Target_Result", None)
                
                if result is not None:
                    if result == 1:
                        st.success("🎉 You're meeting your savings targets!")
                    else:
                        st.warning("⚠️ You're not meeting your savings targets")
                    
                    st.markdown("### Tips to Improve Savings")
                    st.markdown("""
                    - Review discretionary spending (eating out, entertainment)
                    - Consider refinancing loans for better rates
                    - Automate your savings transfers
                    - Look for cheaper insurance options
                    """)
                else:
                    st.error("Could not determine savings efficiency")
            else:
                st.error("❌ Failed to analyze savings efficiency.")

### ✅ Dashboard Views

def dashboard_view():
    """Main dashboard view"""
    st.subheader("📊 Dashboard Overview")
    response = requests.get(f"{BASE_URL}/dashboard/", headers=get_headers())

    if response.status_code == 200:
        data = response.json()
        st.write(f"👋 Welcome back, **{st.session_state.user_email}**!")
        
        # Display quick stats if available
        if "stats" in data:
            cols = st.columns(4)
            cols[0].metric("Current Balance", f"₹{data['stats'].get('balance', 0):,.2f}")
            cols[1].metric("Monthly Income", f"₹{data['stats'].get('income', 0):,.2f}")
            cols[2].metric("Monthly Expenses", f"₹{data['stats'].get('expenses', 0):,.2f}")
            cols[3].metric("Savings Rate", f"{data['stats'].get('savings_rate', 0)}%")
        
        # Navigation based on active section
        if st.session_state.active_section == "profile":
            profile_view()
        elif st.session_state.active_section == "budget":
            budget_view()
        elif st.session_state.active_section == "transactions":
            transactions_view()
        elif st.session_state.active_section == "ai":
            ai_view()
        else:
            # Default dashboard content
            st.markdown("""
                ### Get Started
                Select a section from the sidebar to manage your finances.
            """)
            
            # Quick actions
            st.markdown("### Quick Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💸 Add Transaction"):
                    st.session_state.active_section = "transactions"
                    st.session_state.active_subsection = "log_transaction"
                    st.rerun()
                if st.button("📊 View Budget"):
                    st.session_state.active_section = "budget"
                    st.session_state.active_subsection = "view_budget"
                    st.rerun()
            with col2:
                if st.button("📈 AI Analysis"):
                    st.session_state.active_section = "ai"
                    st.session_state.active_subsection = "expense_prediction"
                    st.rerun()
                if st.button("👤 My Profile"):
                    st.session_state.active_section = "profile"
                    st.session_state.active_subsection = "view_profile"
                    st.rerun()
    else:
        st.error("Failed to load dashboard.")

def add_back_button():
    """Add a back button with unique key"""
    if st.session_state.active_subsection:
        if st.button("⬅️ Back", key=f"back_{st.session_state.active_section}_{st.session_state.active_subsection}"):
            st.session_state.active_subsection = None
            st.rerun()
def add_navigation_buttons():
    """Add navigation buttons with unique keys"""
    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🏠 Dashboard", key="nav_dashboard_btn"):
            st.session_state.active_section = "dashboard"
            st.session_state.active_subsection = None
            st.rerun()
    with col2:
        if st.button("👤 Profile", key="nav_profile_btn"):
            st.session_state.active_section = "profile"
            st.session_state.active_subsection = None
            st.rerun()
    with col3:
        if st.button("💰 Budget", key="nav_budget_btn"):
            st.session_state.active_section = "budget"
            st.session_state.active_subsection = None
            st.rerun()
    with col4:
        if st.button("💳 Transactions", key="nav_transactions_btn"):
            st.session_state.active_section = "transactions"
            st.session_state.active_subsection = None
            st.rerun()
    with col5:
        if st.button("🤖 AI Tools", key="nav_ai_btn"):
            st.session_state.active_section = "ai"
            st.session_state.active_subsection = None
            st.rerun()

def profile_view():
    """Profile management view with unique keys"""
    st.subheader("👤 Profile Management")
    add_back_button()
    
    if st.session_state.active_subsection == "create_profile":
        create_user_profile()
    elif st.session_state.active_subsection == "update_profile":
        update_user_profile()
    elif st.session_state.active_subsection == "delete_profile":
        delete_user_profile()
    else:
        view_user_profile()
        
        st.markdown("### Profile Actions")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("➕ Create Profile", key="profile_create_btn"):
                st.session_state.active_subsection = "create_profile"
                st.rerun()
        with col2:
            if st.button("✏️ Update Profile", key="profile_update_btn"):
                st.session_state.active_subsection = "update_profile"
                st.rerun()
        with col3:
            if st.button("🗑️ Delete Profile", key="profile_delete_btn"):
                st.session_state.active_subsection = "delete_profile"
                st.rerun()
    


def budget_view():
    """Budget management view with unique keys"""
    st.subheader("💰 Budget Management")
    add_back_button()
    
    if st.session_state.active_subsection == "enter_budget":
        enter_budget()
    elif st.session_state.active_subsection == "update_budget":
        update_budget()
    elif st.session_state.active_subsection == "view_budget":
        view_budget()
    elif st.session_state.active_subsection == "delete_budget":
        delete_budget()
    else:
        st.markdown("### Budget Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("➕ Enter Budget", key="budget_enter_btn"):
                st.session_state.active_subsection = "enter_budget"
                st.rerun()
        with col2:
            if st.button("🔄 Update Budget", key="budget_update_btn"):
                st.session_state.active_subsection = "update_budget"
                st.rerun()
        with col3:
            if st.button("👁️ View Budgets", key="budget_view_btn"):
                st.session_state.active_subsection = "view_budget"
                st.rerun()
        with col4:
            if st.button("🗑️ Delete Budget", key="budget_delete_btn"):
                st.session_state.active_subsection = "delete_budget"
                st.rerun()
    
    
def transactions_view():
    """Transactions management view with unique keys"""
    st.subheader("💳 Transactions Management")
    add_back_button()
    
    if st.session_state.active_subsection == "log_transaction":
        log_transaction()
    elif st.session_state.active_subsection == "recurring_transaction":
        recurring_transaction()
    elif st.session_state.active_subsection == "list_transactions":
        list_transactions()
    elif st.session_state.active_subsection == "update_transaction":
        update_transaction()
    elif st.session_state.active_subsection == "delete_transaction":
        delete_transaction()        
    elif st.session_state.active_subsection == "download_reports":
        download_reports()
    else:
        st.markdown("### Transaction Actions")
        # Create 3 columns for better layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Log Transaction", key="txn_log_btn"):
                st.session_state.active_subsection = "log_transaction"
                st.rerun()
            if st.button("📜 List Transactions", key="txn_list_btn"):
                st.session_state.active_subsection = "list_transactions"
                st.rerun()
        
        with col2:
            if st.button("🔄 Recurring Transaction", key="txn_recurring_btn"):
                st.session_state.active_subsection = "recurring_transaction"
                st.rerun()
            if st.button("✏️ Update Transaction", key="txn_update_btn"):
                st.session_state.active_subsection = "update_transaction"
                st.rerun()
        
        with col3:
            if st.button("🗑️ Delete Transaction", key="txn_delete_btn"):
                st.session_state.active_subsection = "delete_transaction"
                st.rerun()
            if st.button("📥 Download Reports", key="txn_download_btn"):
                st.session_state.active_subsection = "download_reports"
                st.rerun()

def ai_view():
    """AI tools view with unique keys"""
    st.subheader("🤖 AI Financial Tools")
    add_back_button()
    
    if st.session_state.active_subsection == "expense_prediction":
        expense_prediction()
    elif st.session_state.active_subsection == "overspending_alert":
        overspending_alert()
    elif st.session_state.active_subsection == "anomaly_detection":
        anomaly_detection()
    elif st.session_state.active_subsection == "financial_score":
        financial_score()
    elif st.session_state.active_subsection == "personalized_recommendations":
        personalized_recommendations()
    elif st.session_state.active_subsection == "savings_efficiency":
        savings_efficiency()
    else:
        st.markdown("""
            ### AI-Powered Financial Insights
            Select an AI tool to get personalized financial analysis and recommendations.
        """)
        
        st.markdown("### Available Tools")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Expense Prediction", key="ai_expense_btn"):
                st.session_state.active_subsection = "expense_prediction"
                st.rerun()
            if st.button("🔍 Anomaly Detection", key="ai_anomaly_btn"):
                st.session_state.active_subsection = "anomaly_detection"
                st.rerun()
            if st.button("💰 Savings Efficiency", key="ai_savings_btn"):
                st.session_state.active_subsection = "savings_efficiency"
                st.rerun()
        with col2:
            if st.button("🚨 Overspending Alert", key="ai_overspending_btn"):
                st.session_state.active_subsection = "overspending_alert"
                st.rerun()
            if st.button("📈 Financial Score", key="ai_score_btn"):
                st.session_state.active_subsection = "financial_score"
                st.rerun()
            if st.button("💡 Personalized Recs", key="ai_recommendations_btn"):
                st.session_state.active_subsection = "personalized_recommendations"
                st.rerun()
    
    

### Main Application
def main():
    """Main application"""
    set_theme()
    
    if st.session_state.access_token:
        # Logged in state
        st.title("💸 Finalyze - Personal Finance Tracker")
        sidebar_navigation()
        dashboard_view()
    else:
        # Not logged in state
        st.title("🔐 Finalyze - Sign In")
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            login_user()
        
        with tab2:
            register_user()

if __name__ == "__main__":
    main()

