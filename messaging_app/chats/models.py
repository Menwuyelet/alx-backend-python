from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, role, password):
        if not first_name or not last_name:
            raise ValueError("First and last name of the user are required.")
        if not email:
            raise ValueError("Email is required.")
        
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, first_name, last_name, email, phone_number, role, password):
        user = self.create_user(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, role=role, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)  
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=250, unique=True, null=False)
    phone_number = models.CharField(max_length=100, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email
    
    @property
    def id(self):
      return self.user_id


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    participants_id = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations_having")
    created_at = models.DateTimeField(auto_now_add=True)

    # participants_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='conversations_having')
   
    def __str__(self):
        return f"Conversation id {self.conversation_id} with user {self.participants_id}"
    

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sent_messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    
    def __str__(self):
        return f"Message id {self.message_id} sent by {self.sender_id}"