from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model


User = get_user_model() # Get the currently active user model


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A ReadOnly ViewSet for viewing User instances.
    Includes search functionality.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

    @action(detail=False, methods=['patch'])
    def update_online_status(self, request):
        is_online = request.data.get('is_online', False)
        request.user.is_online = is_online
        request.user.save()
        return Response({'status': status.HTTP_202_ACCEPTED})


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__first_name','participants__last_name']

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user).distinct()

    def perform_create(self, serializer):
        # This will call the custom create method in ConversationSerializer
        serializer.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    # lookup_field = 'message_id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']

    def get_queryset(self):
        user = self.request.user
        # Filter messages where the current user is a participant in the conversation
        return Message.objects.filter(conversation__participants=user).distinct()

    def perform_create(self, serializer):
        # Automatically set the sender to the current authenticated user
        serializer.save(sender=self.request.user)

