from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Prefetch
from .models import Message
from .serializers import MessageSerializer
from django.core.cache import cache

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    request.user.delete()
    return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threaded_messages_view(request):
    sender=request.user
    cache_key = f'unread_messages_user{sender.id}'
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response(cached_data)

    messages = Message.objects.filter(sender=sender, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender', 'receiver', 'parent_message').prefetch_related('replies')
            )
        )

    serializer = MessageSerializer(messages, many=True, context={'request': request})
    cache.set(cache_key, serializer.data, timeout=60)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_inbox_view(request):
    user=request.user
    unread_messages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'timestamp')
    serializer = MessageSerializer(unread_messages, many=True, context={'request': request})
    return Response(serializer.data)