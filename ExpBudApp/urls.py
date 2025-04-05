from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ExpBudApp.finance_views import BudgetViewSet, TransactionViewSet, RecurringTransactionViewSet
from ExpBudApp.views.auth_views import RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views.export_views import export_transactions_to_csv, export_transactions_to_pdf
from ExpBudApp import views
from .views import analytics_views
from ExpBudApp.Model_Integration.views import unified_prediction_view
from ExpBudApp.views.analytics_views import UserAnalyticsView
from drf_yasg.utils import swagger_auto_schema

# Swagger Schema
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

# Export query parameters (for Swagger)
export_query_params = [
    openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date for the transactions filter (YYYY-MM-DD)", type=openapi.TYPE_STRING),
    openapi.Parameter('end_date', openapi.IN_QUERY, description="End date for the transactions filter (YYYY-MM-DD)", type=openapi.TYPE_STRING),
    openapi.Parameter('category', openapi.IN_QUERY, description="Category of the transaction (e.g., Groceries, Transport)", type=openapi.TYPE_STRING),
    openapi.Parameter('transaction_type', openapi.IN_QUERY, description="Type of the transaction (e.g., Income, Expense)", type=openapi.TYPE_STRING),
    openapi.Parameter('period', openapi.IN_QUERY, description="Period for report generation (weekly, monthly, quarterly, yearly)", type=openapi.TYPE_STRING),
]

# DRF Router
router = DefaultRouter()
router.register(r'budget', BudgetViewSet, basename='budget')
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'recurring-transactions', RecurringTransactionViewSet, basename='recurring-transactions')  # 👈 NEW ROUTE

# URL Patterns
urlpatterns = [
    # 🔐 Auth
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # 💰 Finance APIs
    path('finance/', include(router.urls)),

    # 🤖 AI Predictions
    path('predict-all/', unified_prediction_view, name='predict-all'),

    # 📊 Analytics
    path('analytics/user/', UserAnalyticsView.as_view(), name='user-analytics'),

    # 📄 CSV and PDF Export
    path('export/csv/', export_transactions_to_csv, name='export-transactions-csv'),
    path('export/pdf/', export_transactions_to_pdf, name='export-transactions-pdf'),

    # 📄 Swagger Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
