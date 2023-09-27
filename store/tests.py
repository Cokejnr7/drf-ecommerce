from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from .views import ProductViewSet

# Create your tests here.


class TestProductUrls(SimpleTestCase):
    # for non primary key based operations
    def test_product_list_url_resolves(self):
        url = reverse("products-list")
        self.assertEqual(resolve(url).func.cls, ProductViewSet)

    # for primary key based operations
    def test_product_detail_url_resolves(self):
        url = reverse("products-detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.cls, ProductViewSet)


class TestProductModels(TestCase):
    def test_product_str(self):
        pass
