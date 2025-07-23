from django.shortcuts import render
from rest_framework import status, filters, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ConversationSerializer, UserSerializer, MessageSerializer
from .models import Conversation, User, Message
from .permissions import IsParticipantOrSender
# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOrSender]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        queryset = Conversation.objects.filter(participant_id = self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants_id.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOrSender]
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.filter(sender_id = self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(sender_id=self.request.user)

# class UserCreateViewSet(viewsets.ModelViewSet):
#     permission_classes = [AllowAny]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
    
#     def get_queryset(self):
#         return User.objects.none()
