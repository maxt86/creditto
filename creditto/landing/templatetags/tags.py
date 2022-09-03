from django import template
from social.models import Notification


register = template.Library()

@register.inclusion_tag('social/notifications.html', takes_context=True)
def show_notifications(context):
    user = context['request'].user
    
    notifications = (
        Notification
            .objects
            .filter(receiver=user)
            .exclude(viewed=True)
            .order_by('-date')
    )
    
    return {
        'notifications': notifications,
        'full_path': context['request'].get_full_path(),
    }
