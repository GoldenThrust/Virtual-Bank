from .serializers import UserSerializer
from .models import User
from rest_framework import permissions, generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from notifications.utils import process_notifications
from .utils import get_client_ip
import datetime
import os

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from dotenv import load_dotenv

load_dotenv()


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        user_ip = get_client_ip(request)

        request.data["ip_address"] = user_ip
        response = super().create(request, *args, **kwargs)

        return response


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserUserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)


class UserGet(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserUpdate(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user

        password = request.data.get("password")

        if not (password):
            return Response(
                {"error": "password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid password")

        # notification
        notification_message = "Your profile information has been successfully updated. Your changes are now reflected in your profile."
        process_notifications("admin", "user_notification", notification_message)

        return super().update(request, *args, **kwargs)


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    user_ip = None

    def create(self, request, *args, **kwargs):
        self.user_ip = get_client_ip(request)
        response = super().create(request, *args, **kwargs)

        return response

    def perform_create(self, serializer):
        serializer.save(ip_address=self.user_ip)

        # notification
        notification_message = f"{serializer.validated_data['first_name']} {serializer.validated_data['last_name']} has joined the system"
        process_notifications("admin", "user_notification", notification_message)


class Login(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")
        
        if access_token:
            response.set_cookie("vb_token", access_token, httponly=True)
            response.set_cookie("vb_rtoken", refresh_token, httponly=True)

        return response


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get("access")
        refresh_token = response.data.get("refresh")

        if access_token:
            response.set_cookie("vb_token", access_token, httponly=True)
            response.set_cookie("vb_rtoken", refresh_token, httponly=True)

        return response


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            refresh_token = request.COOKIES.get("vb_rtoken")
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            response = Response({"details": "success"})
            
            response.delete_cookie('vb_token')
            response.delete_cookie('vb_rtoken')
            
            return response
        except Exception as e:
            return Response({"details": "failed"})
