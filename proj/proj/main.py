import streamlit as st
import requests
from auth import authenticate, save_user  # already built this earlier

def main():
    st.set_page_config(page_title="Smart Budget App", page_icon="💰")
    st.sidebar.title("📊 Finalyze")

    menu = [
        "Login / Register",
        "Initial Setup",
        "Enter Budget",
        "Log Transactions",
        "Recurring Expenses",
        "Dashboard",
        "Download Reports",
        "Profile & Settings",
        "Logout"
    ]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Login / Register":
        auth_ui()
    elif choice == "Initial Setup":
        initial_setup_ui()
    elif choice == "Enter Budget":
        budget_entry_ui()
    elif choice == "Log Transactions":
        transaction_ui()
    elif choice == "Recurring Expenses":
        recurring_ui()
    elif choice == "Dashboard":
        dashboard_ui()
    elif choice == "Download Reports":
        report_ui()
    elif choice == "Profile & Settings":
        profile_ui()
    elif choice == "Logout":
        logout_ui()

def auth_ui():
    st.subheader("🔐 Login / Register")
    option = st.radio("Choose:", ["Login", "Register"])

    if option == "Login":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = authenticate(email, password)
            if user:
                st.success("Logged in successfully")
                st.session_state["logged_in"] = True
                st.session_state["access_token"] = user["access"]
                st.session_state["refresh_token"] = user["refresh"]
                st.session_state["user_email"] = email
                st.rerun()
            else:
                st.error("Login failed. Check credentials.")
    else:  # Register
        username = st.text_input("Username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        if st.button("Register"):
            if password != confirm:
                st.warning("Passwords don't match.")
            else:
                success = save_user(email, password, username)
                if success:
                    st.success("Registered! You can log in now.")
                else:
                    st.error("Registration failed.")

def initial_setup_ui():
    st.subheader("📋 Initial Setup – Monthly Financial Inputs")

    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}"
    }

    with st.form("initial_data"):
        income = st.number_input("Monthly Income", step=100.0)
        age = st.number_input("Age", min_value=18, max_value=100)
        dependents = st.number_input("Dependents", min_value=0)
        occupation = st.text_input("Occupation")
        city_tier = st.selectbox("City Tier", [1, 2, 3])

        # Other financial inputs...
        submitted = st.form_submit_button("Submit")
        if submitted:
            payload = {
                "income": income,
                "age": age,
                "dependents": dependents,
                "occupation": occupation,
                "city_tier": city_tier,
                # Add other parameters as needed
            }

            response = requests.post(
                "http://127.0.0.1:8000/api/input-data/create/",
                headers=headers,
                json=payload
            )

            if response.status_code == 201:
                st.success("Initial setup submitted!")
            else:
                st.error("Failed to submit setup.")

def budget_entry_ui():
    st.subheader("📆 Monthly Budget Planning")

    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}"
    }

    with st.form("budget_form"):
        income = st.number_input("Monthly Income", step=100.0)
        savings_goal = st.number_input("Savings Goal", step=100.0)
        month = st.date_input("Budget Month")
        budget_limit = st.number_input("Total Budget Limit")
        category = st.selectbox("Category", [
            "Housing", "Food", "Transportation", "Entertainment", "Utilities", "Health", "Miscellaneous"
        ])

        submit = st.form_submit_button("Save Budget")
        if submit:
            payload = {
                "income": income,
                "savings_goal": savings_goal,
                "month": month.strftime("%Y-%m-%d"),
                "budget_limit": budget_limit,
                "category": category
            }

            response = requests.post(
                "http://127.0.0.1:8000/api/finance/budget/",
                headers=headers,
                json=payload
            )

            if response.status_code == 201:
                st.success("✅ Budget entry saved!")
            else:
                st.error(f"❌ Failed to save budget. {response.status_code} Error")

def transaction_ui():
    st.subheader("🧾 Log Daily Transactions")

    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}"
    }

    with st.form("txn_form"):
        txn_type = st.radio("Type", ["Expense", "Income"])
        category = st.selectbox("Category", [
            "Food", "Travel", "Shopping", "Rent", "Salary", "Health", "Groceries", "EMI", "Utilities", "Others"
        ])
        amount = st.number_input("Amount", min_value=0.0, step=10.0)
        mode = st.selectbox("Mode", ["Cash", "UPI", "Card", "Net Banking"])
        description = st.text_input("Description")
        date = st.date_input("Date")
        time = st.time_input("Time")

        submit = st.form_submit_button("Add Transaction")
        if submit:
            payload = {
                "type": txn_type,
                "category": category,
                "amount": amount,
                "mode": mode,
                "description": description,
                "date": date.strftime("%Y-%m-%d"),
                "time": time.strftime("%H:%M")
            }

            response = requests.post(
                "http://127.0.0.1:8000/api/finance/transactions/",
                headers=headers,
                json=payload
            )

            if response.status_code == 201:
                st.success("✅ Transaction added!")
            else:
                st.error(f"❌ Failed to log transaction. {response.status_code}")

def recurring_ui():
    st.subheader("🔁 Recurring Transactions")

    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}"
    }

    with st.form("recurring_form"):
        name = st.text_input("Transaction Name (e.g., Netflix, Rent, EMI)")
        amount = st.number_input("Amount", min_value=0.0, step=10.0)
        category = st.selectbox("Category", [
            "Rent", "Subscription", "EMI", "Loan", "Health", "Groceries", "Utilities", "Others"
        ])
        start_date = st.date_input("Start Date")
        frequency = st.selectbox("Frequency", ["Monthly", "Weekly", "Yearly"])

        submit = st.form_submit_button("Add Recurring Transaction")

        if submit:
            payload = {
                "name": name,
                "amount": amount,
                "category": category,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "frequency": frequency
            }

            response = requests.post(
                "http://127.0.0.1:8000/api/finance/recurring-transactions/",
                headers=headers,
                json=payload
            )

            if response.status_code == 201:
                st.success("✅ Recurring transaction added!")
            else:
                st.error(f"❌ Failed to save. Status: {response.status_code}")

def dashboard_ui():
    st.subheader("📈 Smart Dashboard (AI Insights)")

    headers = {
        "Authorization": f"Bearer {st.session_state.get('access_token', '')}"
    }

    if st.button("🧠 Generate AI Insights"):
        payload = {
            "user_email": st.session_state.get("user_email", "")
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/predict/",
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                data = response.json()

                st.success("✅ Insights generated!")
                st.markdown(f"### 💡 Forecast: {data.get('monthly_forecast', 'N/A')}")
                st.markdown(f"### 🔴 Overspending Alert: {data.get('overspending_warning', 'N/A')}")
                st.markdown(f"### 💰 Savings Status: {data.get('savings_prediction', 'N/A')}")
                st.markdown(f"### 🧠 Recommendation: {data.get('recommendation', 'N/A')}")
                st.markdown(f"### 📊 Finance Health Score: {data.get('financial_health_score', 'N/A')}")

            else:
                st.error(f"❌ Failed to fetch AI insights. Status {response.status_code}")
        except Exception as e:
            st.error(f"🚫 Error: {e}")

def report_ui():
    st.subheader("📥 Download Financial Reports")

    # Choose report type
    report_type = st.selectbox("Select Report Type", ["CSV", "PDF"])

    if st.button("Download Report"):
        access_token = st.session_state.get("access_token")
        if not access_token:
            st.error("You must be logged in to download reports.")
            return

        headers = {"Authorization": f"Bearer {access_token}"}
        file_format = report_type.lower()

        try:
            response = requests.get(
                f"http://127.0.0.1:8000/api/export/{file_format}/",
                headers=headers
            )

            if response.status_code == 200:
                if file_format == "csv":
                    st.download_button(
                        label="📄 Download CSV",
                        data=response.content,
                        file_name="financial_report.csv",
                        mime="text/csv"
                    )
                elif file_format == "pdf":
                    st.download_button(
                        label="📄 Download PDF",
                        data=response.content,
                        file_name="financial_report.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("❌ Failed to generate report.")
        except Exception as e:
            st.error(f"❌ Error downloading report: {e}")

def profile_ui():
    st.subheader("👤 Profile Settings")
    # User profile settings go here

def logout_ui():
    st.session_state.clear()
    st.success("You have logged out.")
    st.experimental_rerun()

if __name__ == "__main__":
    main()
