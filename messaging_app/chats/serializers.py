from .models import User, Conversation, Message
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number', 'password', 'role']
        read_only_fields = ['user_id']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("The email you provided is already in use. Please use different email.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(source='sender_id', read_only=True)
    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at', 'conversation_id']
        read_only_fields = ['message_id', 'sent_at']
    
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(source='participants_id', read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


