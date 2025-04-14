import os
import joblib
import numpy as np
import pandas as pd

# Get the absolute path to the directory this file is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model and scaler
model = joblib.load(os.path.join(BASE_DIR, 'models','expense_prediction_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR,'models', 'feature_scaler.pkl'))

# Features expected by the model
selected_features = [
    'Income', 'Rent', 'Loan_Repayment', 'Groceries', 'Transport',
    'Eating_Out', 'Entertainment', 'Utilities', 'Healthcare', 'Education',
    'Miscellaneous', 'Savings_Efficiency',
    'Rent_to_Income_Ratio', 'Groceries_to_Income_Ratio',
    'Total_Expenses_to_Income_Ratio'
]

expense_columns = [
    'Rent', 'Groceries', 'Transport', 'Eating_Out', 'Entertainment',
    'Utilities', 'Healthcare', 'Education', 'Miscellaneous'
]

def predict_disposable_income(input_data: dict):
    input_df = pd.DataFrame([input_data])
    scaled_input = scaler.transform(input_df[selected_features])
    disposable_income = model.predict(scaled_input)[0]
    return disposable_income

def calculate_spending_ratios(input_data: dict):
    input_df = pd.DataFrame([input_data])
    total_expenses = input_df[expense_columns].sum(axis=1).values[0]
    spending_ratios = {
        category: input_df[category].values[0] / total_expenses
        for category in expense_columns
    }
    return spending_ratios

def predict_expense_breakdown(input_data: dict):
    disposable_income = predict_disposable_income(input_data)
    total_expenses = input_data['Income'] - disposable_income
    spending_ratios = calculate_spending_ratios(input_data)
    category_expenses = {
        category: total_expenses * ratio
        for category, ratio in spending_ratios.items()
    }

    return {
        'Disposable_Income': round(disposable_income, 2),
        'Total_Expenses': round(total_expenses, 2),
        'Category_Expenses': {
            k: round(v, 2) for k, v in category_expenses.items()
        }
    }
