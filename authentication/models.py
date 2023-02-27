from django.db import models
from django.contrib.auth.models import AbstractBaseUser,UserManager
from django.utils.translation import gettext_lazy as _



# Create your models here.
class CustomManager(UserManager):
    def create(self,email,username,password, **other_fields):
        
        if not email:
            raise ValueError(_('You must provide an email address'))
        if not username:
            raise ValueError(_('You must provide a username'))
        
        email = self.normalize_email(email=email)
        
        user = self.model(email=email,username=username,**other_fields)
        
        user.set_password(password)
        
        user.save()
        
        return user
    
    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned is_superuser=True'))

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned is_staff=True'))

        return self.create_user(email, username, password, **other_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50,unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects = CustomManager()
    
    def __str__(self) -> str:
        return self.username




