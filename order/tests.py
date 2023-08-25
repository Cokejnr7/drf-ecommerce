from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from .views import (
    update_order_paid,
    update_order_status,
    UserListCreateOrderAPIView,
    RetrieveOrderAPIView,
)


# Create your tests here.
class TestUrls(SimpleTestCase):
    def test_update_order_paid_resolves(self):
        url = reverse("update-paid", kwargs={"id": "1"})
        self.assertEquals(resolve(url).func, update_order_paid)

    def test_user_list_create_order_resolves(self):
        url = reverse("user-list-create")
        self.assertEquals(resolve(url).func.view_class, UserListCreateOrderAPIView)

    def test_retrieve_order_resolves(self):
        url = reverse("retrieve-order", kwargs={"id": "1"})
        self.assertEquals(resolve(url).func.view_class, RetrieveOrderAPIView)

    def test_update_order_status_resolves(self):
        url = reverse("update-status", kwargs={"id": "1"})
        self.assertAlmostEquals(resolve(url).func, update_order_status)


class TestModels(TestCase):
    pass
