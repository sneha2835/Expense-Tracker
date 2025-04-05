from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Budget, Transaction
from .serializers import BudgetSerializer, TransactionSerializer

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
    queryset = Transaction.objects.all()  # ✅ Added queryset
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
