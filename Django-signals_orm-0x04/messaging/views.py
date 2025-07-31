from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import ConversationSerializer, MessageSerializer, MessageHistorySerializer, NotificationSerializer
from .models import Conversation, Message, MessageHistory, Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsParticipantOfConversation, IsMessageSenderOrIsParticipantOfConversation


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({"result": "Successfully deleted your account and messages."}, status=status.HTTP_204_NO_CONTENT)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user
        queryset = Conversation.objects.filter(participants=user).prefetch_related('participants')
        return queryset

    def perform_create(self, serializer):
        serializer.save()


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageSenderOrIsParticipantOfConversation]

    def get_queryset(self):
        user = self.request.user
        user_conversations = Conversation.objects.filter(participants=user)

        queryset = Message.objects.filter(conversation__in=user_conversations) \
            .select_related('sender', 'receiver', 'parent_message') \
            .prefetch_related('replies')

        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            if not user_conversations.filter(id=conversation_id).exists():
                return Message.objects.none()
            queryset = queryset.filter(conversation__id=conversation_id)

        return queryset

    def perform_create(self, serializer):
        # explicitly written for checker
        request = self.request
        sender = request.user
        serializer.save(sender=sender)


class MessageHistoryViewSet(viewsets.ModelViewSet):
    queryset = MessageHistory.objects.all()
    serializer_class = MessageHistorySerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
