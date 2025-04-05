from rest_framework import serializers

# Serializer for Expense Prediction Model (RandomForestRegressor)
class ExpensePredictionInputSerializer(serializers.Serializer):
    Income = serializers.FloatField()
    Rent = serializers.FloatField()
    Loan_Repayment = serializers.FloatField()
    Groceries = serializers.FloatField()
    Transport = serializers.FloatField()
    Eating_Out = serializers.FloatField()
    Entertainment = serializers.FloatField()
    Utilities = serializers.FloatField()
    Healthcare = serializers.FloatField()
    Education = serializers.FloatField()
    Miscellaneous = serializers.FloatField()
    Savings_Efficiency = serializers.FloatField()
    Rent_to_Income_Ratio = serializers.FloatField()
    Groceries_to_Income_Ratio = serializers.FloatField()
    Total_Expenses_to_Income_Ratio = serializers.FloatField()

# Serializer for Overspending Alert Model (XGBoostClassifier)
class OverspendingAlertInputSerializer(serializers.Serializer):
    Income = serializers.FloatField()
    Total_Expenses = serializers.FloatField()
    Rent_to_Income_Ratio = serializers.FloatField()
    Groceries_to_Income_Ratio = serializers.FloatField()
    Total_Expenses_to_Income_Ratio = serializers.FloatField()
    Savings_Efficiency = serializers.FloatField()
    Essential_Expenses = serializers.FloatField()
    Non_Essential_Expenses = serializers.FloatField()

# Serializer for Anomaly Detection Model (Isolation Forest)
class AnomalyDetectionInputSerializer(serializers.Serializer):
    Income = serializers.FloatField()
    Total_Expenses = serializers.FloatField()
    Rent_to_Income_Ratio = serializers.FloatField()
    Groceries_to_Income_Ratio = serializers.FloatField()
    Total_Expenses_to_Income_Ratio = serializers.FloatField()
    Savings_Efficiency = serializers.FloatField()
    Discretionary_to_Income_Ratio = serializers.FloatField()
    Savings_Target_Efficiency = serializers.FloatField()

# Serializer for Savings Target and Efficiency Model (DecisionTreeClassifier)
class SavingsTargetEfficiencyInputSerializer(serializers.Serializer):
    Income = serializers.FloatField()
    Disposable_Income = serializers.FloatField()
    Essential_Expenses = serializers.FloatField()
    Non_Essential_Expenses = serializers.FloatField()
    Total_Expenses_to_Income_Ratio = serializers.FloatField()
    Desired_Savings_Percentage = serializers.FloatField()
    Calculated_Savings_Efficiency = serializers.FloatField()
    Potential_Savings_Groceries = serializers.FloatField()
    Potential_Savings_Transport = serializers.FloatField()
    Potential_Savings_Eating_Out = serializers.FloatField()
    Potential_Savings_Entertainment = serializers.FloatField()

# Serializer for Financial Health Score Model (XGBoost Regressor)
class FinancialHealthScoreInputSerializer(serializers.Serializer):
    Income = serializers.FloatField()
    Disposable_Income = serializers.FloatField()
    Essential_Expenses = serializers.FloatField()
    Non_Essential_Expenses = serializers.FloatField()
    Total_Expenses_to_Income_Ratio = serializers.FloatField()
    Desired_Savings_Percentage = serializers.FloatField()
    Savings_Efficiency = serializers.FloatField()
    Debt_to_Income_Ratio = serializers.FloatField()


class PersonalizedSpendingInputSerializer(serializers.Serializer):
    Income = serializers.FloatField()
    Essential_Expenses = serializers.FloatField()
    Discretionary_vs_Essential = serializers.FloatField()
    Savings_Gap = serializers.FloatField()
    Cluster_Label = serializers.IntegerField()