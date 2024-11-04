from django.shortcuts import render
from .serializers import NotificationSerializer
from .models import Notification
from rest_framework import generics, permissions, exceptions
from notifications.paginations import NotifiCationPagination
from rest_framework.exceptions import NotFound

class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = NotifiCationPagination


class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAdminUser]


class UserNotificationList(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = NotifiCationPagination

    def get_queryset(self):
        type = self.request.query_params.get("type", None)
        if type:
            notification_type = f"{type}_notification"
            if notification_type not in [
                "user_notification",
                "account_notification",
                "transaction_notification",
                "security_notification",
            ]:
                raise exceptions.PermissionDenied("Unknown notification type")
            return self.queryset.filter(
                user=self.request.user, notification_type=notification_type.upper()
            )
        return self.queryset.filter(user=self.request.user)


class UserNotificationDetail(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

    def get_object(self):
        queryset = self.get_queryset()
        notification_number = self.kwargs.get("id")

        try:
            notification = queryset.get(id=notification_number)
            print(notification)
        except Notification.DoesNotExist:
            raise NotFound("Notification not found.")

        notification.status = "READ"
        notification.save()

        return notification
