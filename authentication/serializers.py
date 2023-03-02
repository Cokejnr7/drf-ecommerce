from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','id']
        
    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("user with that email already exist")
            
        return super().validate(attrs)
    
    
class UserLoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ["email", "password"]