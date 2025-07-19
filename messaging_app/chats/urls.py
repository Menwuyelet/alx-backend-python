from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet, UserCreateViewSet
from django.urls import path, include
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserCreateViewSet, basename='user')

urlpatterns = router.urls