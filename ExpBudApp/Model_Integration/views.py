import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import UnifiedFinancialInputSerializer
from .utils.feature_engineering import compute_feature_sets

from .expense_prediction import predict_expense_breakdown
from .overspending_alert import predict_overspending_alert
from .anomaly_detection import detect_anomaly
from .savings_efficiency_predictor import predict_savings_efficiency
from .financial_score_predictor import predict_financial_health_score
from .personalized_recommender import generate_spending_recommendation

logger = logging.getLogger(__name__)

# === UNIFIED VIEW ===
@swagger_auto_schema(
    method='post',
    operation_summary="Unified AI Predictions (All-in-One)",
    operation_description="Runs all AI models (expense prediction, anomaly detection, savings efficiency, etc.) and returns a single response.",
    tags=["AI-ML Models"],
    request_body=UnifiedFinancialInputSerializer,
    responses={
        200: openapi.Response(
            description="Combined predictions from all models",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "Expense_Prediction": openapi.Schema(type=openapi.TYPE_OBJECT),
                    "Overspending_Alert": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "Anomaly_Detection": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "Savings_Target_Result": openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    "Financial_Health_Score": openapi.Schema(type=openapi.TYPE_NUMBER),
                    "Personalized_Recommendations": openapi.Schema(type=openapi.TYPE_OBJECT),
                }
            )
        ),
        400: openapi.Response(description="Validation error"),
        500: openapi.Response(description="Prediction failure"),
    }
)
@api_view(['POST'])
def unified_prediction_view(request):
    serializer = UnifiedFinancialInputSerializer(data=request.data)

    if serializer.is_valid():
        user_input = serializer.validated_data
        model_inputs = compute_feature_sets(user_input)

        try:
            results = {
                "Expense_Prediction": predict_expense_breakdown(model_inputs['expense_prediction']),
                "Overspending_Alert": predict_overspending_alert(model_inputs['overspending_alert']),
                "Anomaly_Detection": detect_anomaly(model_inputs['anomaly_detection']),
                "Savings_Target_Result": predict_savings_efficiency(model_inputs['savings_efficiency']),
                "Financial_Health_Score": predict_financial_health_score(model_inputs['financial_health_score']),
                "Personalized_Recommendations": generate_spending_recommendation(model_inputs['personalized_spending']),
            }
            return Response(results, status=200)

        except Exception as e:
            logger.exception("Unified prediction failed")
            return Response({"error": f"Prediction failed: {str(e)}"}, status=500)

    return Response(serializer.errors, status=400)


# === SHARED VIEW HANDLER ===
def process_model_view(request, feature_key, predictor_func, label):
    serializer = UnifiedFinancialInputSerializer(data=request.data)
    if serializer.is_valid():
        try:
            features = compute_feature_sets(serializer.validated_data)
            result = predictor_func(features[feature_key])
            return Response({label: result})
        except Exception as e:
            logger.exception(f"{label} prediction failed")
            return Response({"error": f"{label} prediction failed: {str(e)}"}, status=500)
    return Response(serializer.errors, status=400)


# === INDIVIDUAL MODEL ENDPOINTS ===

@swagger_auto_schema(
    method='post',
    operation_summary="Predict Expense Breakdown",
    operation_description="Uses ML to predict how a user's income will be distributed across categories like food, rent, travel, etc.",
    tags=["AI-ML Models"],
    request_body=UnifiedFinancialInputSerializer,
    responses={200: openapi.Response(description="Predicted expense breakdown")}
)
@api_view(['POST'])
def expense_prediction_view(request):
    return process_model_view(request, 'expense_prediction', predict_expense_breakdown, "Expense_Prediction")


@swagger_auto_schema(
    method='post',
    operation_summary="Detect Overspending Alert",
    operation_description="Predicts if the user is currently overspending based on income, expenses, and habits.",
    tags=["AI-ML Models"],
    request_body=UnifiedFinancialInputSerializer,
    responses={200: openapi.Response(description="True/False overspending alert")}
)
@api_view(['POST'])
def overspending_alert_view(request):
    return process_model_view(request, 'overspending_alert', predict_overspending_alert, "Overspending_Alert")


@swagger_auto_schema(
    method='post',
    operation_summary="Detect Anomaly",
    operation_description="Detects if there's any financial anomaly in the user's expense pattern.",
    tags=["AI-ML Models"],
    request_body=UnifiedFinancialInputSerializer,
    responses={200: openapi.Response(description="Anomaly detection result")}
)
@api_view(['POST'])
def anomaly_detection_view(request):
    return process_model_view(request, 'anomaly_detection', detect_anomaly, "Anomaly_Detection")


@swagger_auto_schema(
    method='post',
    operation_summary="Check Savings Efficiency",
    operation_description="Evaluates whether the user is meeting their savings goals based on current trends.",
    tags=["AI-ML Models"],
    request_body=UnifiedFinancialInputSerializer,
    responses={200: openapi.Response(description="Boolean indicating savings target met or not")}
)
@api_view(['POST'])
def savings_efficiency_view(request):
    return process_model_view(request, 'savings_efficiency', predict_savings_efficiency, "Savings_Target_Result")


@swagger_auto_schema(
    method='post',
    operation_summary="Get Financial Health Score",
    operation_description="Generates a financial health score for the user (e.g. 0–100) based on various financial parameters.",
    tags=["AI-ML Models"],
    request_body=UnifiedFinancialInputSerializer,
    responses={200: openapi.Response(description="Numeric score for financial health")}
)
@api_view(['POST'])
def financial_score_view(request):
    return process_model_view(request, 'financial_health_score', predict_financial_health_score, "Financial_Health_Score")


@swagger_auto_schema(
    method='post',
    operation_summary="Get Personalized Spending Recommendation",
    operation_description="Generates AI-based spending tips and advice tailored to the user's income, savings, and goals.",
    tags=["AI-ML Models"],
    request_body=UnifiedFinancialInputSerializer,
    responses={200: openapi.Response(description="Personalized recommendations object")}
)
@api_view(['POST'])
def personalized_recommendation_view(request):
    return process_model_view(request, 'personalized_spending', generate_spending_recommendation, "Personalized_Recommendations")
