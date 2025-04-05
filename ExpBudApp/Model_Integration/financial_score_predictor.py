import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load(os.path.join(BASE_DIR, 'models','xgboost_fhs_model.pkl'))

features = [
    'Income', 'Disposable_Income', 'Essential_Expenses',
    'Non_Essential_Expenses', 'Total_Expenses_to_Income_Ratio',
    'Desired_Savings_Percentage', 'Savings_Efficiency', 'Debt_to_Income_Ratio'
]

def predict_financial_health_score(input_data: dict):
    input_df = pd.DataFrame([input_data])
    score = model.predict(input_df[features])[0]
    return round(score, 2)
