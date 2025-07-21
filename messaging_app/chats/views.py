from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsSelf, IsConversationParticipant, IsMessageOwnerOrConversationParticipant


User = get_user_model() # Get the currently active user model


class UserViewSet(viewsets.ModelViewSet):
    """
    A ReadOnly ViewSet for viewing User instances.
    Includes search functionality.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsSelf]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name']

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Returns details of the currently authenticated user.
        """
        user_id = request.user.user_id
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsConversationParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__first_name','participants__last_name']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Conversation.objects.filter(participants=user).prefetch_related('participants',
                                                                                                'messages')
        return Conversation.objects.none()

    def perform_create(self, serializer):
        # This will call the custom create method in ConversationSerializer
        serializer.save()


class MessageViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsMessageOwnerOrConversationParticipant]
    # lookup_field = 'message_id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return Message.objects.filter(
                Q(sender=user) | Q(conversation__participants=user)
            ).distinct().select_related('conversation', 'sender')
        return Message.objects.none()

    def perform_create(self, serializer):
        # Automatically set the sender to the current authenticated user
        conversation = serializer.validated_data['conversation']
        if self.request.user not in conversation.participants.all():
            raise serializer.ValidationError("You are not a participant of this conversation.")
        serializer.save(sender=self.request.user)

