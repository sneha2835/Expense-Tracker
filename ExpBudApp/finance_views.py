from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Budget, Transaction, RecurringTransaction
from .serializers import BudgetSerializer, TransactionSerializer, RecurringTransactionSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    """ Viewset for managing user budgets """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    """ Viewset for managing user transactions """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        data = serializer.validated_data

        # Check for existing transaction with same user, merchant, and date
        existing_transaction = Transaction.objects.filter(
            user=user,
            merchant_name=data.get("merchant_name"),
            transaction_date=data.get("transaction_date")
        ).first()

        if existing_transaction:
            # Update the existing transaction
            for attr, value in data.items():
                setattr(existing_transaction, attr, value)
            existing_transaction.save()
        else:
            # Create a new transaction
            serializer.save(user=user)


class RecurringTransactionViewSet(viewsets.ModelViewSet):
    """ Viewset for managing recurring transactions """
    queryset = RecurringTransaction.objects.all()
    serializer_class = RecurringTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RecurringTransaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)