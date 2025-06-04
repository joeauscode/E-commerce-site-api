from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .models import Account
from rest_framework.authtoken.models import Token

from .serializers import (
    RegistrationSerializer,
    AccountSerializer,
)



class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            return Response({
                "message": "Registration successful",
                "user": {
                    "username": account.user.username,
                    "email": account.user.email,
                    "first_name": account.first_name,
                    "last_name": account.last_name,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login_input = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not login_input or not password:
            return Response({"error": "Please provide username/email and password."},
                            status=status.HTTP_400_BAD_REQUEST)

        user_obj = User.objects.filter(Q(username=login_input) | Q(email=login_input)).first()
        if not user_obj:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(username=user_obj.username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"message": "User logged in successfully!", "token": token.key})
        return Response({"error": "Invalid username/email or password."}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            logout(request)
            return Response({"message": "User logged out successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



 # Make sure Account model is imported

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    # GET method to load dashboard data
    def get(self, request):
        try:
            user = request.user  # Get the currently logged-in user
            account = Account.objects.get(user=user)  # Get the account linked to the user
            
            # Prepare the account data
            account_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "avatar_url": account.avatar.url if account.avatar else None,
                "date_created": account.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            }
            # Return the dashboard data in the response
            return Response({"message": "Dashboard loaded successfully", "account": account_data}, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist:
            return Response({"error": "Account not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)