def compute_feature_sets(user_input):
    # Basic derived values
    total_expenses = sum([
        user_input["Rent"],
        user_input["Loan_Repayment"],
        user_input["Insurance"],
        user_input["Groceries"],
        user_input["Transport"],
        user_input["Eating_Out"],
        user_input["Entertainment"],
        user_input["Utilities"],
        user_input["Healthcare"],
        user_input["Education"],
        user_input["Miscellaneous"],
    ])
    
    disposable_income = user_input["Income"] - total_expenses
    desired_savings = (user_input["Desired_Savings_Percentage"] / 100) * user_input["Income"]
    savings_efficiency = (disposable_income / desired_savings) if desired_savings != 0 else 0
    calculated_efficiency = (disposable_income / user_input["Income"]) * 100 if user_input["Income"] != 0 else 0

    # Potential savings (can be estimated, mocked, or calculated via logic if needed)
    potential_savings = {
        "Groceries": user_input["Groceries"] * 0.1,
        "Transport": user_input["Transport"] * 0.1,
        "Eating_Out": user_input["Eating_Out"] * 0.1,
        "Entertainment": user_input["Entertainment"] * 0.1,
        "Utilities": user_input["Utilities"] * 0.05,
        "Healthcare": user_input["Healthcare"] * 0.05,
        "Education": user_input["Education"] * 0.05,
        "Miscellaneous": user_input["Miscellaneous"] * 0.05,
    }

    # Ratios
    rent_ratio = user_input["Rent"] / user_input["Income"] if user_input["Income"] != 0 else 0
    groceries_ratio = user_input["Groceries"] / user_input["Income"] if user_input["Income"] != 0 else 0
    expenses_ratio = total_expenses / user_input["Income"] if user_input["Income"] != 0 else 0
    discretionary = sum([
        user_input["Eating_Out"],
        user_input["Entertainment"],
        user_input["Miscellaneous"]
    ])
    discretionary_ratio = discretionary / user_input["Income"] if user_input["Income"] != 0 else 0
    debt_ratio = (user_input["Loan_Repayment"] + user_input["Insurance"]) / user_input["Income"] if user_input["Income"] != 0 else 0

    # Clustering - can be mocked for now
    cluster_label = 1  # optional k-means clustering prediction

    return {
        "expense_prediction": {
            "Income": user_input["Income"],
            "Rent": user_input["Rent"],
            "Loan_Repayment": user_input["Loan_Repayment"],
            "Groceries": user_input["Groceries"],
            "Transport": user_input["Transport"],
            "Eating_Out": user_input["Eating_Out"],
            "Entertainment": user_input["Entertainment"],
            "Utilities": user_input["Utilities"],
            "Healthcare": user_input["Healthcare"],
            "Education": user_input["Education"],
            "Miscellaneous": user_input["Miscellaneous"],
            "Savings_Efficiency": savings_efficiency,
            "Rent_to_Income_Ratio": rent_ratio,
            "Groceries_to_Income_Ratio": groceries_ratio,
            "Total_Expenses_to_Income_Ratio": expenses_ratio
        },
        "overspending_alert": {
            "Income": user_input["Income"],
            "Total_Expenses": total_expenses,
            "Rent_to_Income_Ratio": rent_ratio,
            "Groceries_to_Income_Ratio": groceries_ratio,
            "Total_Expenses_to_Income_Ratio": expenses_ratio,
            "Savings_Efficiency": savings_efficiency,
            "Essential_Expenses": user_input["Groceries"] + user_input["Transport"] + user_input["Utilities"] + user_input["Healthcare"],
            "Non_Essential_Expenses": discretionary,
        },
        "anomaly_detection": {
            "Income": user_input["Income"],
            "Total_Expenses": total_expenses,
            "Rent_to_Income_Ratio": rent_ratio,
            "Groceries_to_Income_Ratio": groceries_ratio,
            "Total_Expenses_to_Income_Ratio": expenses_ratio,
            "Savings_Efficiency": savings_efficiency,
            "Discretionary_to_Income_Ratio": discretionary_ratio,
            "Savings_Target_Efficiency": calculated_efficiency
        },
        "savings_efficiency": {
            "Income": user_input["Income"],
            "Disposable_Income": disposable_income,
            "Essential_Expenses": user_input["Groceries"] + user_input["Transport"] + user_input["Utilities"] + user_input["Healthcare"],
            "Non_Essential_Expenses": discretionary,
            "Total_Expenses_to_Income_Ratio": expenses_ratio,
            "Desired_Savings_Percentage": user_input["Desired_Savings_Percentage"],
            "Calculated_Savings_Efficiency": calculated_efficiency,
            "Potential_Savings_Groceries": potential_savings["Groceries"],
            "Potential_Savings_Transport": potential_savings["Transport"],
            "Potential_Savings_Eating_Out": potential_savings["Eating_Out"],
            "Potential_Savings_Entertainment": potential_savings["Entertainment"],
        },
        "financial_health_score": {
            "Income": user_input["Income"],
            "Disposable_Income": disposable_income,
            "Essential_Expenses": user_input["Groceries"] + user_input["Transport"] + user_input["Utilities"] + user_input["Healthcare"],
            "Non_Essential_Expenses": discretionary,
            "Total_Expenses_to_Income_Ratio": expenses_ratio,
            "Desired_Savings_Percentage": user_input["Desired_Savings_Percentage"],
            "Savings_Efficiency": savings_efficiency,
            "Debt_to_Income_Ratio": debt_ratio
        },
        "personalized_spending": {
            "Income": user_input["Income"],
            "Essential_Expenses": user_input["Groceries"] + user_input["Transport"] + user_input["Utilities"] + user_input["Healthcare"],
            "Discretionary_vs_Essential": discretionary / (user_input["Groceries"] + user_input["Transport"] + user_input["Utilities"] + user_input["Healthcare"] + 1e-5),
            "Savings_Gap": user_input["Desired_Savings_Percentage"] - calculated_efficiency,
            "Cluster_Label": cluster_label
        }
    }
