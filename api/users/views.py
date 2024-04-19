from .serializers import UserSerializer
from .models import User
from rest_framework import permissions, generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from notifications.utils import process_notifications
from .utils import get_client_ip
import jwt, datetime
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

                token = jwt.encode(payload, os.getenv('JWT_KEY'), algorithm='HS256')
                
                response = Response(
                    {
                        "jwt": token
                    }
                )
                
                response.set_cookie(key='jwt', value=token, httponly=True)
                
                return response
            else:
                raise AuthenticationFailed("Account disactivated")
        else:
            raise AuthenticationFailed("User not found!")


class VerifyUser(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            payload = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("expired cookie")
        
        user  = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class Logout(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        response = Response(
            {
                "details": "success"
            }
        )
        response.delete_cookie('jwt')
        
        return response