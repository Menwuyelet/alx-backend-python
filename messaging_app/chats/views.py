from django.shortcuts import render
from rest_framework import status, filters, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ConversationSerializer, UserSerializer, MessageSerializer
from .models import Conversation, User, Message
from .permissions import IsParticipantOrSender, IsParticipantOfConversation
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
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
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['timestamp'] 

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Message.objects.none()

        if self.request.user not in conversation.participants.all():
            return Message.objects.none()

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = Conversation.objects.get(id=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not authorized to send a message in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
