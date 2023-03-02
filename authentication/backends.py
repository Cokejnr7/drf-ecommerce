from rest_framework import authentication,exceptions
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request)
        
        if not auth:
            return
        
        prefix,token = auth.decode('utf-8').split(" ")
        
        if prefix !='Bearer':
            raise exceptions.AuthenticationFailed("Expected Bearer token type")
        
        try:
            payload = jwt.decode(token,settings.JWT_SECRET_KEY,algorithms=[settings.ALGORITHM,])
            user = User.objects.get(email=payload['email'])
            
            return user
            
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("invalid token")
        
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("token expired")