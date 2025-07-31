from rest_framework import serializers
from .models import Conversation, Message, MessageHistory, Notification
from django.contrib.auth.models import User

class UserSerializerForMessage(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class RecursiveMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializerForMessage(read_only=True)
    # Don't include 'replies' here if you're trying to flatten the recursion to a single level for initial fetch
    # or you'll need to control depth carefully.
    # For now, let's just show basic info for recursive replies.
    # If you want deeply nested replies, you'll use MessageSerializer itself recursively.
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'edited', 'parent_message', 'read']


class MessageSerializer(serializers.ModelSerializer):
    sender_info = UserSerializerForMessage(source='sender', read_only=True)
    receiver_info = UserSerializerForMessage(source='receiver', read_only=True)
    replies = RecursiveMessageSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'timestamp']

    def validate(self, data):
        request_user = self.context['request'].user
        conversation = data.get('conversation')

        # Check if the user is a participant in the conversation
        if conversation and request_user not in conversation.participants.all():
            raise serializers.ValidationError(
                {"detail": "You can only send messages in conversations you are part of."}
            )

        # Ensure the message has a conversation:
        if not conversation:
            raise serializers.ValidationError(
                {"conversation": "This field is required."}
            )

        return data


class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        read_only=False
    )
    participants_info = UserSerializerForMessage(source='participants', many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'participants_info', 'name', 'messages', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        participants = data.get('participants')
        request_user = self.context['request'].user

        # 1. Check if the number of participants is exactly two
        if len(participants) != 2:
            raise serializers.ValidationError(
                {"participants": "A conversation must have exactly two participants."}
            )

        # 2. Check that the authenticated user is one of the participants
        if request_user not in participants:
            raise serializers.ValidationError(
                {"participants": "You must be a participant in the conversation you are creating."}
            )

        # 3. Check that a conversation with these two participants doesn't already exist
        other_user = [user for user in participants if user != request_user][0]
        existing_conversation = Conversation.objects.filter(
            participants=request_user
        ).filter(
            participants=other_user
        ).first()

        if existing_conversation:
            raise serializers.ValidationError(
                {"participants": f"A conversation with user '{other_user.username}' already exists."}
            )

        # return the validated data
        return data

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation


class MessageHistorySerializer(serializers.ModelSerializer):
    edited_by = UserSerializerForMessage(read_only=True)

    class Meta:
        model = MessageHistory
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    receiver = UserSerializerForMessage(read_only=True)
    # You might want to represent the associated message details
    message = RecursiveMessageSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
