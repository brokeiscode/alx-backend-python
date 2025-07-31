from django.urls import path, include
from . import views
from .views import ConversationViewSet, MessageViewSet, MessageHistoryViewSet, NotificationViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'messagehistories', MessageHistoryViewSet, basename='messagehistory')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path(r'', include(router.urls)),
    path('delete-account/', views.delete_user, name='delete-account'),
    path('api-auth/', include('rest_framework.urls')), # For browsable API login/logout
]
