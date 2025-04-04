import joblib
import pandas as pd
import os

# Define model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models','personalized_spending_recommender.pkl')

# Load the model
model = joblib.load(MODEL_PATH)

# Define features used by the model
FEATURE_COLUMNS = ['Income', 'Essential_Expenses', 'Discretionary_vs_Essential', 'Savings_Gap', 'Cluster_Label']

# Define recommendation logic
def generate_spending_recommendation(user_input):
    user_df = pd.DataFrame([user_input], columns=FEATURE_COLUMNS)
    predicted_savings_percentage = model.predict(user_df)[0]

    income = user_input['Income']
    cluster = user_input['Cluster_Label']

    if cluster == 0:
        recommendations = {
            'Rent': income * 0.20,
            'Groceries': income * 0.15,
            'Savings': income * (predicted_savings_percentage / 100),
            'Discretionary': income * 0.10
        }
    elif cluster == 1:
        recommendations = {
            'Rent': income * 0.25,
            'Groceries': income * 0.15,
            'Savings': income * (predicted_savings_percentage / 100),
            'Discretionary': income * 0.10
        }
    else:
        recommendations = {
            'Rent': income * 0.30,
            'Groceries': income * 0.20,
            'Savings': income * (predicted_savings_percentage / 100),
            'Discretionary': income * 0.15
        }

    # Round and return
    return {k: round(float(v), 2) for k, v in recommendations.items()}