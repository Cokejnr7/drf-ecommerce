from django.test import SimpleTestCase
from helpers.utils import url_resolve
from .views import UserCreateView, UserLoginView, refresh_token_view

# Create your tests here.


class TestUrls(SimpleTestCase):
    def test_user_register_resolves(self):
        self.assertEqual(url_resolve("register").func.view_class, UserCreateView)

    def test_user_login_resolves(self):
        self.assertEqual(url_resolve("login").func.view_class, UserLoginView)

    def test_refresh_token_resolves(self):
        self.assertEqual(url_resolve("refresh").func, refresh_token_view)
