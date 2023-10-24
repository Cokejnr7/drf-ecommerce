from rest_framework import permissions
from .models import BlackListedToken


class IsTokenValid(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True
        access_token = request.auth.decode("utf-8")
        refresh_token = request.COOKIES.get("refresh_token")
        print(access_token)
        try:
            is_blackListed = BlackListedToken.objects.get(
                user=user_id, refresh_token=refresh_token
            )
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
