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