from .models import Notification
from users.models import User

def process_notifications(user, type, message):
    if type not in ['user_notification', 'account_notification', 'transaction_notification', 'security_notification']:
        raise Exception('Unknown notification type')

    users_to_notify = User.objects.filter(is_superuser=True) if user == 'admin' else [user]

    for target_user in users_to_notify:
        if type == 'user_notification':
            send_user_notification(target_user, message)
        elif type == 'account_notification':
            send_account_notification(target_user, message)
        elif type == 'transaction_notification':
            send_transaction_notification(target_user, message)
        elif type == 'security_notification':
            send_security_notification(target_user, message) 


def send_user_notification(user, message):
    Notification.objects.create(user=user, notification_type='USER_NOTIFICATION', content=message)

def send_account_notification(user, message):
    Notification.objects.create(user=user, notification_type='ACCOUNT_NOTIFICATION', content=message)

def send_transaction_notification(user, message):
    Notification.objects.create(user=user, notification_type='TRANSACTION_NOTIFICATION', content=message)

def send_security_notification(user, message):
    Notification.objects.create(user=user, notification_type='SECURITY_NOTIFICATION', content=message)
