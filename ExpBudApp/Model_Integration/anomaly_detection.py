import os
import joblib
import pandas as pd

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR,'models', 'isolation_forest_model.pkl')
anomaly_model = joblib.load(model_path)

# Features used in training
anomaly_features = [
    'Income', 'Total_Expenses', 'Rent_to_Income_Ratio',
    'Groceries_to_Income_Ratio', 'Total_Expenses_to_Income_Ratio',
    'Savings_Efficiency', 'Discretionary_to_Income_Ratio',
    'Savings_Target_Efficiency'
]

def detect_anomaly(input_data: dict):
    df = pd.DataFrame([input_data])
    prediction = anomaly_model.predict(df[anomaly_features])
    return prediction[0] == -1  # True if anomaly
