from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=instance, receiver=instance.receiver)

@receiver(pre_save, sender=Message)
def messagehistory_pre_save(sender, instance, **kwargs):
    if instance.id is None:
        pass
    try:
        previous = Message.objects.get(id=instance.id)
        if previous:
            MessageHistory.objects.create(message=instance, old_content=previous.content)
    except Message.DoesNotExist:
        return f"Instance does not exist"
