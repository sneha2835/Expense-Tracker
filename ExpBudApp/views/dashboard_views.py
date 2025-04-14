from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from django.contrib.auth import get_user_model

from ExpBudApp.models import UserProfile
from ExpBudApp.serializers import UserProfileSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

# ✅ 1. Main dashboard (feature overview)
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'post', 'get', 'delete']

    @swagger_auto_schema(
        operation_summary="Get dashboard overview with feature links",
        tags=["2. User Dashboard"]
    )
    def get(self, request):
        user = request.user
        base_url = "/api/"

        return Response({
            "message": f"Welcome, {user.username}!",
            "features": {
                "Your Profile": {
                    "View Profile": f"{base_url}dashboard/profile/",
                    "Create Profile": f"{base_url}dashboard/profile/create/",
                    "Update Profile": f"{base_url}dashboard/profile/update/",
                    "Delete Profile": f"{base_url}dashboard/profile/delete/",
                },
                "Input Your Financial Data": f"{base_url}inputs/create/",
                "View Your Inputs": f"{base_url}inputs/list/",

                "Expense Breakdown": f"{base_url}predict/expense-breakdown/",
                "Overspending Alert": f"{base_url}predict/overspending-alert/",
                "Savings Target Efficiency": f"{base_url}predict/savings-target-efficiency/",
                "Financial Health Score": f"{base_url}predict/financial-health-score/",
                "Anomaly Detection": f"{base_url}predict/anomaly-detection/",
                "Spending Recommendations": f"{base_url}predict/recommendations/"
            }
        }, status=status.HTTP_200_OK)


# ✅ 3. View user profile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Get logged-in user's profile",
        tags=["2. User Dashboard"]
    )
    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

class CreateUserProfileView(APIView):
    """Allows a logged-in user to create a profile."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new user profile",
        request_body=UserProfileSerializer,
        tags=["2. User Dashboard"]
    )
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ 4. Update profile
class UpdateUserProfileView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    @swagger_auto_schema(
        operation_summary="Update logged-in user's profile",
        tags=["2. User Dashboard"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    
# ✅ 5. Delete profile
class DeleteUserProfileView(generics.DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Delete logged-in user's profile",
        tags=["2. User Dashboard"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
