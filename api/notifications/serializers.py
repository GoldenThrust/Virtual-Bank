from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "notification_type",
            "content",
            "status",
            "created_date",
        ]

        extra_kwargs = {
            "notification_type": {"read_only": True},
            "content": {"read_only": True},
        }
