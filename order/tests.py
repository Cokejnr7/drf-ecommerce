from django.test import SimpleTestCase, TestCase
from helpers.utils import url_resolve
from .views import (
    update_order_paid,
    update_order_status,
    UserListCreateOrderAPIView,
    RetrieveOrderAPIView,
)


# Create your tests here.
class TestUrls(SimpleTestCase):
    def test_update_order_paid_resolves(self):
        self.assertEquals(
            url_resolve("update-paid", kwargs={"id": "1"}).func, update_order_paid
        )

    def test_user_list_create_order_resolves(self):
        self.assertEquals(
            url_resolve("user-list-create").func.view_class,
            UserListCreateOrderAPIView,
        )

    def test_retrieve_order_resolves(self):
        self.assertEquals(
            url_resolve("retrieve-order", kwargs={"id": "1"}).func.view_class,
            RetrieveOrderAPIView,
        )

    def test_update_order_status_resolves(self):
        self.assertAlmostEquals(
            url_resolve("update-status", kwargs={"id": "1"}).func, update_order_status
        )


class TestModels(TestCase):
    pass
