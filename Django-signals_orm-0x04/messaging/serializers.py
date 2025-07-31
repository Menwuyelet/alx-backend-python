from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class MessageSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'parent_message', 'replies']
        read_only_fields = ['id', 'sender','timestamp', 'edited']

    def get_replies(self, obj):
        queryset = obj.replies.all().select_related('parent_message').prefetch_related('replies')
        return MessageSerializer(queryset, many=True, context=self.context).data