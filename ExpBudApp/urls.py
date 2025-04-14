from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions

# Swagger Schema
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Auth Views
from ExpBudApp.views.auth_views import RegisterView, CustomTokenObtainPairView

# Dashboard Views
from ExpBudApp.views.dashboard_views import (
    DashboardView,
    UserProfileView,
    CreateUserProfileView,
    UpdateUserProfileView,
    DeleteUserProfileView,
)

# Finance Views
from ExpBudApp.finance_views import (
    BudgetViewSet,
    TransactionViewSet,
    RecurringTransactionViewSet,
    NotificationListView,
    NotificationUpdateView,
    OverspendingAlertView,
    AIPredictionView,
)

# Input Data Views
from ExpBudApp.views.input_views import (
    CreateUserInputDataView,
    ListUserInputDataView,
)

# Export Views
from ExpBudApp.views.export_views import (
    ExportTransactionsCSV,
    ExportTransactionsPDF,
)

# Model Integration Views (AI Predictions)
from ExpBudApp.Model_Integration.views import (
    unified_prediction_view,
    expense_prediction_view,
    overspending_alert_view,
    anomaly_detection_view,
    savings_efficiency_view,
    financial_score_view,
    personalized_recommendation_view,
)

# Optional (if used in urls)
from ExpBudApp.views.dashboard_views import DashboardView

# Swagger Schema Setup
schema_view = get_schema_view(
    openapi.Info(
        title="Expense Budget App API",
        default_version="v1",
        description="API documentation for Expense Budget App",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="support@yourapp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# DRF Router for Finance APIs
router = DefaultRouter()
router.register(r'budget', BudgetViewSet, basename='budget')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'recurring-transactions', RecurringTransactionViewSet, basename='recurring-transactions')

# Main URL Patterns
urlpatterns = [
    # 🔐 Auth
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # 👤 User Profile
    path('dashboard/profile/', UserProfileView.as_view(), name="user-profile"),
    path('dashboard/profile/update/', UpdateUserProfileView.as_view(), name="update-user-profile"),
    path('dashboard/profile/delete/', DeleteUserProfileView.as_view(), name="delete-user-profile"),
    path('dashboard/profile/create/', CreateUserProfileView.as_view(), name="create-user-profile"),

    # 📊 Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # 🧠 Input Data
    path('input-data/create/', CreateUserInputDataView.as_view(), name='create-input-data'),
    path('input-data/history/', ListUserInputDataView.as_view(), name='list-input-data'),

    # 💸 Finance APIs
    path('finance/', include([
        path('', include(router.urls)),
        path('notifications/', NotificationListView.as_view(), name='notifications-list'),
        path('notifications/update/', NotificationUpdateView.as_view(), name='notifications-update'),
    ])),

    # 🤖 AI Predictions
    path('predict/', unified_prediction_view, name='unified_prediction'),

    path('predict/expense/', expense_prediction_view, name='expense_prediction'),
    path('predict/overspending/', overspending_alert_view, name='overspending_alert'),
    path('predict/anomaly/', anomaly_detection_view, name='anomaly_detection'),
    path('predict/savings/', savings_efficiency_view, name='savings_efficiency'),
    path('predict/score/', financial_score_view, name='financial_score'),
    path('predict/recommendation/', personalized_recommendation_view, name='personalized_recommendation'),

    # ⬇️ Export
    path('export/csv/', ExportTransactionsCSV.as_view(), name='export_csv'),
    path('export/pdf/', ExportTransactionsPDF.as_view(), name='export_pdf'),

    # ⚙️ User Settings
    path('ai-prediction/', AIPredictionView.as_view(), name='ai-prediction'),

    # 🚨 Alerts
    path('alerts/overspending/', OverspendingAlertView.as_view(), name='overspending-alert'),

    # 📚 API Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
