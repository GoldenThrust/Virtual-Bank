from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from transactions.models import Transaction
from notifications.models import Notification
from notifications.serializers import NotificationSerializer
from transactions.serializers import TransactionSerializer
import json

@receiver(post_save, sender=Transaction)
def debitcard_created(sender, instance, created, **kwargs):
    serializer  = TransactionSerializer(instance)
    json_data = json.dumps(serializer.data)

    if created:
        channel_layer = get_channel_layer()

        user_id = instance.payer.user.id
        partner_id = instance.payee.user.id

        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                "type": "send_transaction",
                "data": json_data
            },
        )

        async_to_sync(channel_layer.group_send)(
            f"user_{partner_id}",
            {
                "type": "send_transaction",
                "data": json_data
            },
        )



@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    channel_layer = get_channel_layer()
    user_id = instance.user.id

    serializer  = NotificationSerializer(instance)
    json_data = json.dumps(serializer.data)

    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "data": json_data
        },
    )
