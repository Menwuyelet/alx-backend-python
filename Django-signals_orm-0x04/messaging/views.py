from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.generics import DestroyAPIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class UserDeletView(DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    
    def get_object(self):
        return self.request.user  