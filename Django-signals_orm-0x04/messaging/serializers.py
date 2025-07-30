from rest_framework import serializers
from .models import Message, MessageHistory, Notification


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class MessageHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageHistory
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
