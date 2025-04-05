from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from datetime import date

# ------------------------
# Custom User Model
# ------------------------

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# ------------------------
# Transaction Model
# ------------------------

class Transaction(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('UPI', 'UPI'),
        ('Other', 'Other'),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    transaction_date = models.DateField(default=now)
    transaction_time = models.TimeField(default=now)
    merchant_name = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    transaction_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - ₹{self.amount}"


# ------------------------
# Recurring Transaction Model
# ------------------------

class RecurringTransaction(models.Model):
    FREQUENCY_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('UPI', 'UPI'),
        ('Other', 'Other'),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    start_date = models.DateField(default=now)
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, default='Monthly')
    next_due_date = models.DateField(default=now)
    merchant_name = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Cash')

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.frequency})"


# ------------------------
# Budget Model
# ------------------------

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - ₹{self.budget_limit}"


# ------------------------
# Savings Goal Model
# ------------------------

class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"{self.user.username} - {self.goal_name}"


# ------------------------
# AI Prediction Model
# ------------------------

class AIPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    predicted_expense = models.DecimalField(max_digits=10, decimal_places=2)
    prediction_date = models.DateField(default=now)
    prediction_type = models.CharField(
        max_length=50,
        choices=[
            ('Expense Forecast', 'Expense Forecast'),
            ('Savings Forecast', 'Savings Forecast'),
            ('Anomaly Detection', 'Anomaly Detection'),
        ],
        default='Expense Forecast'
    )
    confidence_score = models.FloatField(null=True, blank=True)
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction_type}"


# ------------------------
# Overspending Alert Model
# ------------------------

class OverspendingAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    alert_type = models.CharField(
        max_length=50,
        choices=[
            ('Overspending', 'Overspending'),
            ('Unusual Transaction', 'Unusual Transaction'),
        ],
        default='Overspending'
    )
    alert_message = models.TextField()
    alert_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.email} - {self.category} - {self.alert_type}"


# ------------------------
# Financial Report Model
# ------------------------

class FinancialReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(
        max_length=50,
        choices=[
            ('Monthly Summary', 'Monthly Summary'),
            ('Yearly Report', 'Yearly Report'),
        ],
        default='Monthly Summary'
    )
    report_data = models.JSONField()
    generated_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.email} - {self.report_type}"