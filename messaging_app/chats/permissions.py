from rest_framework import permissions

class IsParticipantOrSender(permissions.BasePermission):
    """
    Only allow users to access their own conversations/messages.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if hasattr(obj, 'participants_id'):
            return user in obj.participants_id.all()
        elif hasattr(obj, 'sender_id'):
            return obj.sender_id == user
        return False


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access or modify its messages.
    """

    def has_permission(self, request, view):
        # Only allow if user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS + ("PUT", "PATCH", "DELETE"):
            return request.user in obj.conversation.participants.all()
        return False