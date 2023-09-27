from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


# Create your models here.
class CustomManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address."))

        email = self.normalize_email(email)

        user = self.model(email=email, **other_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must be assigned is_superuser=True"))

        if other_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must be assigned is_staff=True"))

        return self.create_user(email, password, **other_fields)


AUTH_PROVIDERS = {"email": "email", "google": "google"}


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    auth_provider = models.CharField(
        max_length=100, default=AUTH_PROVIDERS.get("email")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["auth_provider"]

    objects = CustomManager()

    def __str__(self) -> str:
        return self.email


# class BlackListedToken(models.Model):
#     access_token = models.CharField(max_length=500)
#     refresh_token = models.CharField(max_length=500)
#     user = models.ForeignKey(
#         CustomUser, related_name="token_user", on_delete=models.CASCADE
#     )
#     timestamp = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("access_token", "refresh_token", "user")
