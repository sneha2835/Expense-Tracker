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

@swagger_auto_schema(
    method='post',
    operation_summary="Unified AI Predictions",
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
            return Response({"error": f"Prediction failed: {str(e)}"}, status=500)

    return Response(serializer.errors, status=400)
