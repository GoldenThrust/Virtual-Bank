from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(read_only=True)


    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'content', 'status', 'created_date']