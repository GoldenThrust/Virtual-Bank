from django.db import models
from users.models import User
from accounts.models import Account

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('OVERDUE', 'Overdue'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    payee = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment ID: {self.pk} - Payee: {self.payee.username} - Status: {self.get_status_display()}"
