from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"
    
class Notification(models.Model):
    messages = models.OneToOneField(Message, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"Notification for {self.user} from message {self.message.id}"
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='edit_history')

    def __str__(self):
        return f"Message id {self.message.id} - updated at {self.edited_at}"
    