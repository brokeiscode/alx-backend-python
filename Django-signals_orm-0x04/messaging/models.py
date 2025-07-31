from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    name = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Conversation room'
        db_table = 'conversations'

    def __str__(self):
        usernames = " - ".join([user.username for user in self.participants.all()])
        return self.name if self.name else f"{usernames} Chat"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_receiver')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name='replies')
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Chat Message'
        db_table = 'messages'

    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # custom

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}..."


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='messagehistory')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-edited_at']
        verbose_name = 'Message History'
        db_table = 'messagehistories'

    def __str__(self):
        return f"OLD MESSAGE: {self.old_content}"


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
