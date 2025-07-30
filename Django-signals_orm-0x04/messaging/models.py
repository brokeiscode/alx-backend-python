from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Chat Message'
        db_table = 'messages'

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='messagehistory')
    old_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notify_receiver')
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message Notification'
        db_table = 'notifications'

    def __str__(self):
        return f"{self.created_at}: New Message"
