from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import joblib
import os
import pandas as pd

from .serializers import (
    ExpensePredictionInputSerializer,
    OverspendingAlertInputSerializer,
    AnomalyDetectionInputSerializer,
    FinancialHealthScoreInputSerializer,
    PersonalizedSpendingInputSerializer
)

from .anomaly_detection import detect_anomaly
from .overspending_alert import predict_overspending_alert
from .savings_efficiency_predictor import predict_savings_efficiency, FEATURE_COLUMNS
from .financial_score_predictor import predict_financial_health_score
from .personalized_recommender import generate_spending_recommendation


# Load model and scaler for expense prediction
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, 'models', 'expense_prediction_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'models','feature_scaler.pkl'))

expected_features = [
    'Income', 'Rent', 'Loan_Repayment', 'Groceries', 'Transport',
    'Eating_Out', 'Entertainment', 'Utilities', 'Healthcare', 'Education',
    'Miscellaneous', 'Savings_Efficiency',
    'Rent_to_Income_Ratio', 'Groceries_to_Income_Ratio',
    'Total_Expenses_to_Income_Ratio'
]


class ExpensePredictionView(APIView):

    @swagger_auto_schema(
        operation_summary="Expense Prediction",
        tags=["AI-ML Models"],
        request_body=ExpensePredictionInputSerializer,
        responses={200: openapi.Response(
            description='Predicted Disposable Income',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'predicted_disposable_income': openapi.Schema(type=openapi.TYPE_NUMBER)
                }
            )
        )}
    )
    def post(self, request):
        serializer = ExpensePredictionInputSerializer(data=request.data)
        if serializer.is_valid():
            input_data = serializer.validated_data
            input_df = pd.DataFrame([input_data])
            scaled_input = scaler.transform(input_df)
            prediction = model.predict(scaled_input)
            return Response({'predicted_disposable_income': prediction[0]}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OverspendingAlertView(APIView):

    @swagger_auto_schema(
        operation_summary="Overspending Alert",
        tags=["AI-ML Models"],
        request_body=OverspendingAlertInputSerializer,
        responses={200: openapi.Response(
            description='Overspending Alert',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'overspending_alert': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        )}
    )
    def post(self, request):
        serializer = OverspendingAlertInputSerializer(data=request.data)
        if serializer.is_valid():
            input_data = serializer.validated_data
            alert = predict_overspending_alert(input_data)
            return Response({'overspending_alert': alert}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnomalyDetectionView(APIView):

    @swagger_auto_schema(
        operation_summary="Anomaly Detection",
        tags=["AI-ML Models"],
        request_body=AnomalyDetectionInputSerializer,
        responses={200: openapi.Response(
            description='Anomaly Detection Result',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'anomaly': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        )}
    )
    def post(self, request):
        serializer = AnomalyDetectionInputSerializer(data=request.data)
        if serializer.is_valid():
            input_data = serializer.validated_data
            is_anomaly = detect_anomaly(input_data)
            return Response({'anomaly': is_anomaly}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavingsTargetEfficiency(APIView):

    @swagger_auto_schema(
        operation_summary="Savings Target Efficiency",
        tags=["AI-ML Models"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={field: openapi.Schema(type=openapi.TYPE_NUMBER) for field in FEATURE_COLUMNS},
            required=FEATURE_COLUMNS
        ),
        responses={200: openapi.Response(
            description='Savings Target Achievement Prediction',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Savings_Target_Achieved': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                }
            )
        )}
    )
    def post(self, request):
        try:
            data = request.data
            missing = [field for field in FEATURE_COLUMNS if field not in data]
            if missing:
                return Response({"error": f"Missing fields: {missing}"}, status=400)

            prediction = predict_savings_efficiency(data)
            return Response({"Savings_Target_Achieved": prediction}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class FinancialHealthScoreView(APIView):

    @swagger_auto_schema(
        operation_summary="Financial Health Score",
        tags=["AI-ML Models"],
        request_body=FinancialHealthScoreInputSerializer,
        responses={200: openapi.Response(
            description="Predicted Financial Health Score",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "financial_health_score": openapi.Schema(type=openapi.TYPE_NUMBER)
                }
            )
        )}
    )
    def post(self, request):
        serializer = FinancialHealthScoreInputSerializer(data=request.data)
        if serializer.is_valid():
            score = predict_financial_health_score(serializer.validated_data)
            return Response({"financial_health_score": score}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonalizedSpendingRecommendationView(APIView):

    @swagger_auto_schema(
        operation_summary="Personalized Spending Recommendation",
        tags=["AI-ML Models"],
        request_body=PersonalizedSpendingInputSerializer,
        responses={200: openapi.Response(
            description="Spending Recommendations",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "recommendations": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        additional_properties=openapi.Schema(type=openapi.TYPE_NUMBER)
                    )
                }
            )
        )}
    )
    def post(self, request):
        serializer = PersonalizedSpendingInputSerializer(data=request.data)
        if serializer.is_valid():
            input_data = serializer.validated_data
            recommendations = generate_spending_recommendation(input_data)
            return Response({"recommendations": recommendations}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
