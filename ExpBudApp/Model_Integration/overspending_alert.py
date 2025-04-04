import os
import joblib
import pandas as pd

# Get the absolute path to this file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the trained XGBoost model
overspending_model = joblib.load(os.path.join(BASE_DIR, 'models','overspending_alert_model.pkl'))

# Features used by the model
alert_features = [
    'Income', 'Total_Expenses', 'Rent_to_Income_Ratio',
    'Groceries_to_Income_Ratio', 'Total_Expenses_to_Income_Ratio',
    'Savings_Efficiency', 'Essential_Expenses', 'Non_Essential_Expenses'
]

def predict_overspending_alert(input_data: dict) -> bool:
    """
    Predict whether the user is overspending.
    """
    input_df = pd.DataFrame([input_data])
    prediction = overspending_model.predict(input_df[alert_features])
    return bool(prediction[0])
