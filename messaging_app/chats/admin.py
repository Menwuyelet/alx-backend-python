from django.contrib import admin
from .models import User, Conversation, Message
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name') 
@admin.register(Conversation)
class ConversationRegister(admin.ModelAdmin):
    list_display = ('id',)

@admin.register(Message)
class MessageRegister(admin.ModelAdmin):
    list_display = ('id', 'sender__first_name')