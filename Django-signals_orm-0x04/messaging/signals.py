from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=instance, user=instance.receiver)

@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Message.objects.get(pk=instance.pk)
        if old_instance.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=old_instance.content, edited_by=instance.sender)
            instance.edited = True

@receiver(post_delete, sender=User)
def clean_up(sender, instance):
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()