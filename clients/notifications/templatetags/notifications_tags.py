from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def unread_notifications_count(context):
    from notifications.models import Notification

    user = context['request'].user
    if user.is_authenticated:
        return Notification.objects.select_related('user').filter(user=user, status='UNREAD').count()
    return 0

@register.simple_tag(takes_context=True)
def unread_notification(context):
    from notifications.models import Notification

    user = context['request'].user
    if user.is_authenticated:
        return Notification.objects.select_related('user').filter(user=user, status='UNREAD').order_by('-created_date')[:50]
    return 0