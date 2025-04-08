# ExpBudApp/views/input_views.py

from rest_framework import generics, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ExpBudApp.models import UserInputProfile
from ExpBudApp.serializers import UserInputProfileSerializer


# ✅ 1. Submit financial input data
class CreateUserInputDataView(generics.CreateAPIView):
    serializer_class = UserInputProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_id="submitUserInputData",
        operation_summary="Submit financial input data",
        operation_description=(
            "Use this endpoint to submit financial input data like income, expenses, ratios, etc. "
            "This data will be used across all prediction models."
        ),
        tags=["3. Input & Expenses"],
        request_body=UserInputProfileSerializer,
        responses={201: openapi.Response("Input data created", UserInputProfileSerializer)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ 2. List all user input records
class ListUserInputDataView(generics.ListAPIView):
    serializer_class = UserInputProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_id="listUserInputData",
        operation_summary="List all submitted input records",
        operation_description=(
            "Returns a list of previously submitted financial input data for the logged-in user, "
            "ordered by the most recent submission."
        ),
        tags=["3. Input & Expenses"],
        responses={200: openapi.Response("List of input data", UserInputProfileSerializer(many=True))}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return UserInputProfile.objects.filter(user=self.request.user).order_by('-created_at')
