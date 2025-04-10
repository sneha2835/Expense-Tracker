from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.core.validators import MinValueValidator
from datetime import date
from django.utils import timezone
from decimal import Decimal
# ----------------------------
# Custom User & User Manager
# ----------------------------


AUTH_PROVIDERS = [
    ('email', 'Email'),
    ('google', 'Google'),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=20, choices=AUTH_PROVIDERS, default='email')
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


# ----------------------------
# Financial Models
# ----------------------------

class Budget(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    income = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    savings_goal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    month = models.DateField(help_text="Any date in the month you're budgeting for", default=date.today)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],default=Decimal('0.00'))
    category = models.CharField(max_length=50, default="General")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.month.strftime('%B %Y')} | {self.category} | ₹{self.budget_limit}"


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
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    category = models.CharField(max_length=50, default="General")
    transaction_date = models.DateField(default=date.today)
    transaction_time = models.TimeField(default=now)
    merchant_name = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    transaction_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.category} - ₹{self.amount}"


class RecurringTransaction(models.Model):
    FREQUENCY_CHOICES = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]
    PAYMENT_METHOD_CHOICES = Transaction.PAYMENT_METHOD_CHOICES

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    category = models.CharField(max_length=50, default="General")
    start_date = models.DateField(default=date.today)
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, default='Monthly')
    next_due_date = models.DateField(default=date.today)
    merchant_name = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Cash')

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.frequency})"


class OverspendingAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, default="General")
    limit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], default=Decimal('0.00'))
    current_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    alert_triggered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.category} alert"


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class FinancialReport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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


class AIPrediction(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    predicted_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prediction_date = models.DateField(default=date.today)
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

    def __str__(self):
        return f"{self.user.username} - {self.prediction_type}"


# ----------------------------
# User Profile & Input Models
# ----------------------------

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class UserInputProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='input_profile')

    income = models.DecimalField(max_digits=10, decimal_places=2,  validators=[MinValueValidator(Decimal('0.0'))])
    age = models.IntegerField(default=0)
    dependents = models.IntegerField(default=0)
    occupation = models.CharField(max_length=100, default="Not Specified")
    city_tier = models.IntegerField(default=1)

    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    loan_repayment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    groceries = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    eating_out = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    entertainment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    utilities = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    healthcare = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    education = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    miscellaneous = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    savings_efficiency = models.FloatField(default=0)
    rent_to_income_ratio = models.FloatField(default=0)
    groceries_to_income_ratio = models.FloatField(default=0)
    total_expenses_to_income_ratio = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_ratios(self):
        try:
            income = float(self.income)
            total_expenses = float(
                self.rent + self.loan_repayment + self.groceries +
                self.transport + self.eating_out + self.entertainment +
                self.utilities + self.healthcare + self.education + self.miscellaneous
            )

            self.total_expenses_to_income_ratio = total_expenses / income if income else 0
            self.rent_to_income_ratio = float(self.rent) / income if income else 0
            self.groceries_to_income_ratio = float(self.groceries) / income if income else 0
            self.savings_efficiency = 1 - self.total_expenses_to_income_ratio

        except Exception as e:
            raise ValueError(f"Error calculating ratios: {e}")

    def save(self, *args, **kwargs):
        self.calculate_ratios()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - User Input Profile"
