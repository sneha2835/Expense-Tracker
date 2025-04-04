from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ExpBudApp.finance_views import BudgetViewSet, TransactionViewSet
from ExpBudApp.views.auth_views import RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# ML model views
from ExpBudApp.Model_Integration.views import (
    ExpensePredictionView,
    OverspendingAlertView,
    AnomalyDetectionView,
    SavingsTargetEfficiency,
    FinancialHealthScoreView,
    PersonalizedSpendingRecommendationView,  
)

# Router for finance
router = DefaultRouter()
router.register(r'budget', BudgetViewSet, basename='budget')
router.register(r'transactions', TransactionViewSet, basename='transactions')

# Swagger schema setup
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

# URL patterns
urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # Finance
    path('finance/', include(router.urls)),

    # AI/ML Endpoints
    # AI/ML Endpoints
    path('predict-expenses/', ExpensePredictionView.as_view(), name='predict-expenses'),
    path('predict-overspending/', OverspendingAlertView.as_view(), name='predict-overspending'),
    path('predict-anomaly/', AnomalyDetectionView.as_view(), name='predict-anomaly'),
    path('predict-savings-target/', SavingsTargetEfficiency.as_view(), name='predict-savings-target'),
    path('predict-financial-health/', FinancialHealthScoreView.as_view(), name='predict-financial-health'),
    path('predict-spending-recommendation/', PersonalizedSpendingRecommendationView.as_view(), name='predict-spending-recommendation'),

    # Swagger Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
