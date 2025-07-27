from django.shortcuts import render
from rest_framework import status, filters, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ConversationSerializer, UserSerializer, MessageSerializer
from .models import Conversation, User, Message
from .permissions import IsParticipantOrSender, IsParticipantOfConversation
from rest_framework.exceptions import PermissionDenied, NotFound, APIException
from rest_framework.response import Response
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOrSender]
    serializer_class = ConversationSerializer
    lookup_field = 'id'
    def get_queryset(self):
        queryset = Conversation.objects.filter(participants = self.request.user)
        return queryset
        # Modify the above queryset to select the messages in the convo ensuring the requesting user is participant in that convo.
    
    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['timestamp'] 
    lookup_field = 'id'

    def get_queryset(self):
        conversation = self.kwargs.get("conversation_id")
        try:
            conversation = Conversation.objects.get(id=conversation)
        except Conversation.DoesNotExist:
            return Message.objects.none()


        if self.request.user not in conversation.participants.all():
            ex = APIException("You are not authorized to access this conversation.")
            ex.status_code = status.HTTP_403_FORBIDDEN
            raise ex

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        print("KWARGS:", self.kwargs)
        conversation_id = self.kwargs.get("conversation_id")
        print(f"debug: {conversation_id}")
        if not conversation_id:
            raise NotFound("Conversation ID is missing.")
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation does not exist.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not authorized to send a message in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)

