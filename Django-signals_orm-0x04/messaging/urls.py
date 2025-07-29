from django.urls import path, include
from .views import MessageViewSet, NotificationViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'messages', MessageViewSet, basename='message')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path(r'', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')), # For browsable API login/logout
]