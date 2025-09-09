import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer



# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "code": status.HTTP_201_CREATED,
                "message": "User registered successfully",
                "data": serializer.data
            }
            return Response(response_data, status.HTTP_201_CREATED)

        raise ValidationError(serializer.errors)


# login view with access token, user id and email in response
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                refresh = RefreshToken.for_user(user)
                response_data = {
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "user_id": user.id,
                    "email": user.email,
                    "access": str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({
                    "success": False,
                    "message": "Invalid credentials",
                    "status": status.HTTP_401_UNAUTHORIZED
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            "success": False,
            "message": "Login failed",
            "data": serializer.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)





# Profile View
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        response = {
            "status": status.HTTP_200_OK,
            "success": True,
            "data": serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Profile updated successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Profile update failed",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Logout successful. Please delete the access token from client."
        }, status=status.HTTP_200_OK)
