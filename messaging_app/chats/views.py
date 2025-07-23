from django.shortcuts import render
from rest_framework import status, filters, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ConversationSerializer, UserSerializer, MessageSerializer
from .models import Conversation, User, Message
from .permissions import IsParticipantOrSender, IsParticipantOfConversation
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
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

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_id")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
                return Response(
                    {"detail": "You are not authorized to access this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )

        if self.request.user not in conversation.participants.all():
                return Response(
                    {"detail": "You are not authorized to access this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = Conversation.objects.get(id=conversation_id)

        if self.request.user not in conversation.participants.all():
                return Response(
                    {"detail": "You are not authorized to access this conversation."},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer.save(sender=self.request.user, conversation=conversation)

