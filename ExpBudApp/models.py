from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.core.validators import MinValueValidator

# ----------------------------
# Custom User & User Manager
# ----------------------------

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

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


# ----------------------------
# Financial Models
# ----------------------------

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
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=50)
    transaction_date = models.DateField(default=now)
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
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=50)
    start_date = models.DateField(default=now)
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, default='Monthly')
    next_due_date = models.DateField(default=now)
    merchant_name = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Cash')

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.frequency})"


class Budget(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.category} - ₹{self.budget_limit}"


class SavingsGoal(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    current_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    deadline = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.goal_name}"


class OverspendingAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    limit = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
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


class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    currency = models.CharField(max_length=10, default='USD')
    theme = models.CharField(max_length=10, default='light')

    def __str__(self):
        return f"{self.user.username}'s settings"


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

    def __str__(self):
        return f"{self.user.username} - {self.prediction_type}"


# ----------------------------
# User Profile & Input Models
# ----------------------------

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.full_name


class UserInputProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='input_profile')

    # Core financial fields
    income = models.DecimalField(max_digits=10, decimal_places=2)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    loan_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    groceries = models.DecimalField(max_digits=10, decimal_places=2)
    transport = models.DecimalField(max_digits=10, decimal_places=2)
    eating_out = models.DecimalField(max_digits=10, decimal_places=2)
    entertainment = models.DecimalField(max_digits=10, decimal_places=2)
    utilities = models.DecimalField(max_digits=10, decimal_places=2)
    healthcare = models.DecimalField(max_digits=10, decimal_places=2)
    education = models.DecimalField(max_digits=10, decimal_places=2)
    miscellaneous = models.DecimalField(max_digits=10, decimal_places=2)

    # Precomputed fields for ML
    savings_efficiency = models.FloatField()
    rent_to_income_ratio = models.FloatField()
    groceries_to_income_ratio = models.FloatField()
    total_expenses_to_income_ratio = models.FloatField()

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
