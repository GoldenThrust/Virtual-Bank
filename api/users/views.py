from .serializers import UserSerializer
from .models import User
from rest_framework import permissions, generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from notifications.utils import process_notifications
from .utils import get_client_ip
import datetime
import os
# from dotenv import load_dotenv
# load_dotenv()


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
        process_notifications(
            "admin", "user_notification", notification_message)

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
        process_notifications(
            "admin", "user_notification", notification_message)


class Login(APIView):
    # queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")

        if user is not None:
            if user.is_active:
                payload = {
                    "id": user.id,
                    "exp": datetime.datetime.now() + datetime.timedelta(minutes=60),
                    "iat": datetime.datetime.utcnow()
                }

                return response
            else:
                raise AuthenticationFailed("Account disactivated")
        else:
            raise AuthenticationFailed("User not found!")


class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
        {
                    "details": "success"
                }
            )
        except Exception as e:
            return Response(
                {
                    "details": "success"
                }
            )