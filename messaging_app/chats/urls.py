from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]