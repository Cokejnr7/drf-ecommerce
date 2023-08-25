from django.test import SimpleTestCase
from django.urls import resolve, reverse
from .models import Order, OrderItem

# Create your tests here.


class TestUrls(SimpleTestCase):
    def setUp(self):
        pass

    def test_update_order_paid_resolves(self):
        url = reverse("update-paid")

        print(url)
