from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def message_post_save(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=instance, receiver=instance.receiver)

@receiver(pre_save, sender=Message)
def messagehistory_pre_save(sender, instance, **kwargs):
    if instance.id is None:
        pass
    try:
        current = instance
        previous = Message.objects.get(id=instance.id)
        if previous.content!= current.content:
            MessageHistory.objects.create(message=instance, old_content=previous.content, edited_by=current.sender)
    except Message.DoesNotExist:
        return f"Instance does not exist"

@receiver(post_delete, sender=User)
def deleteuser_post_delete(sender, instance, **kwargs):
    # delete all messages the user was associated with.
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    # delete all notification which the user received.
    Notification.objects.filter(receiver=instance).delete()
    # delete all message history which the user edited.
    MessageHistory.objects.filter(edited_by=instance).delete()
