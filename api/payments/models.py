from django.db import models
from users.models import User
from accounts.models import Account
from transactions.models import Transaction

class Payment(models.Model):
    # STATUS_CHOICES = [
    #     ('PAID', 'Paid'),
    #     ('PENDING', 'Pending'),
    #     ('OVERDUE', 'Overdue'),
    # ]

    # transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, related_name='payment')
    # payee = models.ForeignKey(User, on_delete=models.CASCADE)
    # due_date = models.DateTimeField()
    # status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    # def __str__(self):
    #     return f"Payment ID: {self.pk} - Payee: {self.payee.username} - Status: {self.get_status_display()}"
    pass
