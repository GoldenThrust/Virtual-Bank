from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from deposits.models import Deposit
from transfers.models import Transfer
from debit_cards.models import DebitCardTransaction
from notifications.models import Notification


@receiver(post_save, sender=Deposit)
def deposit_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        user_id = instance.transaction.account.user.id

        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_transaction",
                "data": {
                    "amount": float(instance.transaction.amount),
                    "date": instance.transaction.date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "type": instance.transaction.transaction_type,
                },
            },
        )


@receiver(post_save, sender=Transfer)
def transfer_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        user_id = instance.transaction.account.user.id
        partner_id = instance.transaction_partner_account.user.id

        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_transaction",
                "data": {
                    "amount": float(instance.transaction.amount),
                    "date": instance.transaction.date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "user": "You",
                    "type": instance.transaction.transaction_type,
                },
            },
        )

        async_to_sync(channel_layer.group_send)(
            f"user_{partner_id}",
            {
                "type": "send_transaction",
                "data": {
                    "amount": float(instance.transaction.amount),
                    "date": instance.transaction.date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "user": instance.transaction.account.user.get_full_name(),
                    "type": instance.transaction.transaction_type,
                },
            },
        )


@receiver(post_save, sender=DebitCardTransaction)
def debitcard_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()

        user_id = instance.transaction.account.user.id
        partner_id = instance.transaction_partner_account.user.id

        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_transaction",
                "data": {
                    "amount": float(instance.transaction.amount),
                    "date": instance.transaction.date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "user": "You",
                    "type": instance.transaction.transaction_type,
                },
            },
        )

        async_to_sync(channel_layer.group_send)(
            f"user_{partner_id}",
            {
                "type": "send_transaction",
                "data": {
                    "amount": float(instance.transaction.amount),
                    "date": instance.transaction.date.strftime("%Y-%m-%dT%H:%M:%S"),
                    "user": instance.transaction.account.user.get_full_name(),
                    "type": instance.transaction.transaction_type,
                },
            },
        )


@receiver(post_save, sender=Notification)
def debitcard_created(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()

    user_id = instance.user.id

    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "message": {
                "content": instance.content,
                "notification_type": instance.get_notification_type_display(),
            },
        },
    )
