from django.db import models
from users.models import User


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("USER_NOTIFICATION", "User Notification"),
        ("TRANSACTION_NOTIFICATION", "Transaction Alert"),
        ("ACCOUNT_NOTIFICATION", "Account Alert"),
        ("SECURITY_NOTIFICATION", "Security Notification"),
    ]

    STATUS_CHOICES = [
        ("READ", "Read"),
        ("UNREAD", "Unread"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    content = models.TextField()
    status = models.CharField(max_length=10, default='UNREAD', choices=STATUS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Notification ID: {self.pk} - Type: {self.get_notification_type_display()} - User: {self.user.username}"
