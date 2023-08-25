from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import ProductViewSet

# Create your tests here.


class TestUrls(SimpleTestCase):
    def test_product_url_resolves(self):
        url = reverse("products")
        print(url)
