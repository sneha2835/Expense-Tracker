from rest_framework import serializers, generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import (
    Budget, Transaction, RecurringTransaction, Notification,
    OverspendingAlert, AIPrediction, UserProfile, UserInputProfile
)

User = get_user_model()

# ------------------------
# Authentication Serializers
# ------------------------

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Remove first_name, last_name
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": False, "allow_null": True},
            "last_name": {"required": False, "allow_null": True},
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

# ------------------------
# Financial Models Serializers
# ------------------------

class BudgetSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True) 
    class Meta:
        model = Budget
        fields = '__all__'
        read_only_fields = ['user']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['user']

class RecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransaction
        fields = '__all__'
        read_only_fields = ['user']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['user']

class OverspendingAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverspendingAlert
        fields = '__all__'
        read_only_fields = ['user']

class AIPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPrediction
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)  # hides from required fields

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user','created_at']

class UserInputProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInputProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

# ------------------------
# Dashboard Serializer (Non-model)
# ------------------------

class DashboardSerializer(serializers.Serializer):
    income_total = serializers.FloatField()
    expense_total = serializers.FloatField()
    savings = serializers.FloatField()
    goal_amount = serializers.FloatField(allow_null=True)
    progress_percent = serializers.FloatField()

# ------------------------
# ML Output Serializers
# ------------------------

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
    is_overspending = serializers.CharField()
    anomaly_status = serializers.CharField()
    target_achieved = serializers.CharField()
    financial_health_score = serializers.FloatField()
    recommendations = serializers.DictField(child=serializers.FloatField())

# ------------------------
# Create or Update View (for UserInput)
# ------------------------

class UserInputCreateOrUpdateView(generics.CreateAPIView):
    serializer_class = UserInputProfileSerializer
    queryset = UserInputProfile.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        instance, created = UserInputProfile.objects.update_or_create(
            user=user,
            defaults=serializer.validated_data
        )
        serializer.instance = instance
