from .models import Notification
from users.models import User
def send_user_notification(user, message):
    if user == 'admin':
        admin = User.objects.filter(is_superuser=True)
        for user in admin:
            Notification.objects.create(user=user, notification_type='USER_NOTIFICATION', content=message)
    else:
        Notification.objects.create(user=user, notification_type='USER_NOTIFICATION', content=message)

def send_account_notification(user, message):
    pass

def send_transaction_notification(user, message):
    pass

def send_security_notification(user, message):
    pass