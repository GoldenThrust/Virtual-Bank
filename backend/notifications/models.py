from django.db import models
from users.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('TRANSACTION_ALERT', 'Transaction Alert'),
        ('ACCOUNT_UPDATE', 'Account Update'),
        ('SECURITY_NOTIFICATION', 'Security Notification'),
    ]

    STATUS_CHOICES = [
        ('READ', 'Read'),
        ('UNREAD', 'Unread'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification ID: {self.pk} - Type: {self.get_type_display()} - User: {self.user.username}"
