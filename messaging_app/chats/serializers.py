from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    conservations = serializers.HyperlinkedRelatedField(many=True, view_name='conversation-details')

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'bio', 'is_online', 'conversations']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ['url', 'id', 'conversation', 'sender', 'message_body', 'sent_at', 'is_read']
        read_only_fields = ['sender', 'sent_at']


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['url', 'id', 'name', 'created_at', 'participants']
        read_only_fields = ['created_at']

    def get_messages(self, obj):
        messages = obj.messages.order_by('sent_at')
        return MessageSerializer(messages, many=True).data
