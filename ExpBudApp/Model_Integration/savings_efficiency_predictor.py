import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models','decision_tree_model.pkl')

# Load model once
model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = [
    'Income', 'Disposable_Income', 'Essential_Expenses', 'Non_Essential_Expenses',
    'Total_Expenses_to_Income_Ratio', 'Desired_Savings_Percentage', 'Calculated_Savings_Efficiency',
    'Potential_Savings_Groceries', 'Potential_Savings_Transport',
    'Potential_Savings_Eating_Out', 'Potential_Savings_Entertainment'
]

def predict_savings_efficiency(data_dict):
    """
    data_dict: Dictionary of user financial inputs matching FEATURE_COLUMNS.
    Returns: 0 or 1 (whether savings target is achieved)
    """
    X = np.array([[data_dict[col] for col in FEATURE_COLUMNS]])
    prediction = model.predict(X)[0]
    return int(prediction)
