from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import CustomUser
# Create your views here.

class UserModelViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
