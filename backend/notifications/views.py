from django.shortcuts import render
from .serializers import NotificationSerializer
from .models import Notification
from rest_framework import generics, permissions, exceptions

class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]

class UserNotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class UserNotificationDetailList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'type'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, notification_type=self.kwargs['type'].upper())


class UserNotificationDetail(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'notification_number'

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-created_date')
    
    def get_object(self):
        queryset = self.get_queryset()
        notification_number = self.kwargs.get('notification_number') 

        try:
            notification = queryset[int(notification_number) - 1]
        except (IndexError, ValueError):
            return []
        
        notification.status = 'READ'
        notification.save()

        return notification