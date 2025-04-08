from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas
from io import BytesIO
import random
from datetime import date

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    Budget, Transaction, RecurringTransaction, SavingsGoal,
    Notification, UserSettings, OverspendingAlert, AIPrediction
)
from .serializers import (
    BudgetSerializer, TransactionSerializer, RecurringTransactionSerializer,
    SavingsGoalSerializer, NotificationSerializer, UserSettingsSerializer,
    OverspendingAlertSerializer, AIPredictionSerializer
)

# ✅ 3. Budget Planning
class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["4. Budget Planning"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ 4. Transaction Management
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["5. Transactions"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data
        existing_transaction = Transaction.objects.filter(
            user=user,
            merchant_name=data.get("merchant_name"),
            transaction_date=data.get("transaction_date")
        ).first()
        if existing_transaction:
            for attr, value in data.items():
                setattr(existing_transaction, attr, value)
            existing_transaction.save()
        else:
            serializer.save(user=user)


# ✅ 4. Recurring Transactions
class RecurringTransactionViewSet(viewsets.ModelViewSet):
    serializer_class = RecurringTransactionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["6. Recurring Expenses"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return RecurringTransaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ 5. Savings Goals
class SavingsGoalViewSet(viewsets.ModelViewSet):
    serializer_class = SavingsGoalSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["7. Savings & Goals"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return SavingsGoal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ 6. Notifications (List + Update)
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["10. Notifications"],
        operation_summary="List notifications",
        manual_parameters=[
            openapi.Parameter('unread', openapi.IN_QUERY, description="true/false", type=openapi.TYPE_BOOLEAN)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Notification.objects.filter(user=self.request.user)
        unread = self.request.query_params.get('unread')
        if unread is not None:
            if unread.lower() == 'true':
                queryset = queryset.filter(read=False)
            elif unread.lower() == 'false':
                queryset = queryset.filter(read=True)
        return queryset


class NotificationUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["10. Notifications"],
        operation_summary="Update notifications",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER)),
                'mark_as_read': openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
            required=['ids']
        )
    )
    def post(self, request):
        ids = request.data.get('ids', [])
        mark_as_read = request.data.get('mark_as_read', True)

        if not isinstance(ids, list):
            return Response({'error': 'ids should be a list of notification IDs'}, status=status.HTTP_400_BAD_REQUEST)

        notifications = Notification.objects.filter(id__in=ids, user=request.user)
        updated_count = notifications.update(read=mark_as_read)

        return Response({
            'message': f'{updated_count} notification(s) updated.',
            'updated_ids': ids
        })


# ✅ 7. User Settings
class UserSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["12. User Settings"])
    def get(self, request):
        settings, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["12. User Settings"],
        request_body=UserSettingsSerializer
    )
    def put(self, request):
        settings, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Settings updated", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ 8. Overspending Alerts
class OverspendingAlertView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(tags=["9. Alerts & Warnings"])
    def get(self, request):
        alerts = OverspendingAlert.objects.filter(user=request.user)
        triggered = alerts.filter(alert_triggered=True)
        serializer = OverspendingAlertSerializer(triggered, many=True)
        return Response({"overspending_alerts": serializer.data})

    @swagger_auto_schema(
        tags=["9. Alerts & Warnings"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["category", "limit", "current_spent"],
            properties={
                "category": openapi.Schema(type=openapi.TYPE_STRING),
                "limit": openapi.Schema(type=openapi.TYPE_NUMBER),
                "current_spent": openapi.Schema(type=openapi.TYPE_NUMBER),
            }
        )
    )
    def post(self, request):
        category = request.data.get('category')
        limit = request.data.get('limit')
        current_spent = request.data.get('current_spent')

        if not category or limit is None or current_spent is None:
            return Response({
                "error": "Please provide 'category', 'limit', and 'current_spent'."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            limit = float(limit)
            current_spent = float(current_spent)
        except ValueError:
            return Response({
                "error": "'limit' and 'current_spent' must be numbers."
            }, status=status.HTTP_400_BAD_REQUEST)

        alert, _ = OverspendingAlert.objects.get_or_create(
            user=request.user, category=category,
            defaults={'limit': limit, 'current_spent': current_spent}
        )

        alert.limit = limit
        alert.current_spent = current_spent
        alert.alert_triggered = current_spent > limit
        alert.save()

        serializer = OverspendingAlertSerializer(alert)
        return Response({
            "message": "Overspending check completed.",
            "alert_triggered": alert.alert_triggered,
            "data": serializer.data
        })


# ✅ 9. Export Transactions (CSV & PDF)
class ExportTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["11. Export Data"],
        manual_parameters=[
            openapi.Parameter(
                'format',
                openapi.IN_QUERY,
                description="Export format: csv or pdf",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        format = request.query_params.get('format', 'csv').lower()
        transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')

        if format == 'csv':
            return self._export_csv(transactions)
        elif format == 'pdf':
            return self._export_pdf(transactions)
        else:
            return Response({'error': 'Invalid format. Use ?format=csv or ?format=pdf'}, status=status.HTTP_400_BAD_REQUEST)

    def _export_csv(self, transactions):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Date', 'Time', 'Amount', 'Category', 'Merchant', 'Payment Method', 'Description'])
        for txn in transactions:
            writer.writerow([
                txn.transaction_date, txn.transaction_time, txn.amount, txn.category,
                txn.merchant_name or '', txn.payment_method, txn.transaction_description or ''
            ])
        return response

    def _export_pdf(self, transactions):
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica", 10)
        p.drawString(100, 820, "Transaction History")

        y = 800
        for txn in transactions:
            text = f"{txn.transaction_date} | ₹{txn.amount} | {txn.category} | {txn.payment_method}"
            p.drawString(40, y, text)
            y -= 20
            if y < 40:
                p.showPage()
                y = 800

        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')


# ✅ 10. AI Predictions (Placeholder)
class AIPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["8. AI Predictions"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "prediction_type": openapi.Schema(type=openapi.TYPE_STRING, default="Expense Forecast")
            }
        )
    )
    def post(self, request):
        prediction_type = request.data.get("prediction_type", "Expense Forecast")
        predicted_value = round(random.uniform(1000, 5000), 2)
        confidence_score = round(random.uniform(0.7, 0.99), 2)

        prediction = AIPrediction.objects.create(
            user=request.user,
            predicted_expense=predicted_value,
            prediction_type=prediction_type,
            prediction_date=date.today(),
            confidence_score=confidence_score
        )

        serializer = AIPredictionSerializer(prediction)
        return Response({
            "message": f"{prediction_type} prediction generated.",
            "data": serializer.data
        })
