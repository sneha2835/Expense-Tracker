from rest_framework import serializers
from .models import (
    Budget, Transaction, RecurringTransaction,
    SavingsGoal, Notification, UserSettings,
    OverspendingAlert, AIPrediction, UserProfile, UserInputProfile
)
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Budget Serializer
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['user']

# Transaction Serializer — fixed the typo in fields
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'  # corrected from '_all_'
        read_only_fields = ['user']

# Recurring Transaction Serializer
class RecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransaction
        fields = '__all__'
        read_only_fields = ['user']


from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "password", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": False, "allow_null": True},
            "last_name": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




# Savings Goal Serializer
class SavingsGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsGoal
        fields = '__all__'
        read_only_fields = ['user']

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user']

# User Serializer
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# Custom Token Serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

# User Settings Serializer
class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = '__all__'
        read_only_fields = ['user']

# Overspending Alert Serializer
class OverspendingAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverspendingAlert
        fields = '__all__'
        read_only_fields = ['user']

# Dashboard Serializer (non-model serializer)
class DashboardSerializer(serializers.Serializer):
    income_total = serializers.FloatField()
    expense_total = serializers.FloatField()
    savings = serializers.FloatField()
    goal_amount = serializers.FloatField(allow_null=True)
    progress_percent = serializers.FloatField()


class TransactionExportCSVView(serializers.ModelSerializer):
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)

        # Create the HTTP response with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Amount', 'Category', 'Date', 'Merchant Name', 'Description'])

        for tx in transactions:
            writer.writerow([
                tx.id,
                tx.amount,
                tx.category,
                tx.transaction_date,
                tx.merchant_name,
                tx.description
            ])

        return response
    
class AIPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPrediction
        fields = '__all__'    

# ------------------------
# Custom JWT Token Serializer
# ------------------------

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token


# ------------------------
# User Profile Serializer
# ------------------------

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']


# ------------------------
# User Input Profile Serializer
# ------------------------

class UserInputDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInputProfile
        exclude = ['user', 'created_at']  # Assigned automatically


# -------------------------------------------------
# ML Model Output Serializers for Swagger + Output
# -------------------------------------------------

class ExpenseBreakdownOutputSerializer(serializers.Serializer):
    Disposable_Income = serializers.FloatField()
    Total_Expenses = serializers.FloatField()
    Category_Expenses = serializers.DictField(child=serializers.FloatField())


class OverspendingAlertOutputSerializer(serializers.Serializer):
    is_overspending = serializers.CharField()  # Yes/No


class AnomalyDetectionOutputSerializer(serializers.Serializer):
    anomaly_status = serializers.CharField()  # Yes/No


class SavingsTargetEfficiencyOutputSerializer(serializers.Serializer):
    target_achieved = serializers.CharField()  # Yes/No


class FinancialHealthScoreOutputSerializer(serializers.Serializer):
    score = serializers.FloatField()


class SpendingRecommendationOutputSerializer(serializers.Serializer):
    Rent = serializers.FloatField()
    Groceries = serializers.FloatField()
    Savings = serializers.FloatField()
    Discretionary = serializers.FloatField()


class UnifiedMLPredictionOutputSerializer(serializers.Serializer):
    disposable_income = serializers.FloatField()
    total_expenses = serializers.FloatField()
    category_expenses = serializers.DictField(child=serializers.FloatField())

    is_overspending = serializers.CharField()  # "Yes" or "No"
    anomaly_status = serializers.CharField()   # "Yes" or "No"
    target_achieved = serializers.CharField()  # "Yes" or "No"

    financial_health_score = serializers.FloatField()

    recommendations = serializers.DictField(
        child=serializers.FloatField()
    )
