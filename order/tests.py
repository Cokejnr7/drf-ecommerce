from django.test import SimpleTestCase, TestCase
from helpers.utils import url_resolve
from .views import (
    update_order_paid,
    update_order_status,
    UserListCreateOrderAPIView,
    RetrieveOrderAPIView,
)
from store.models import Product
from .models import Order, OrderItem
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from decouple import config


User = get_user_model()


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


class TestOrderModel(TestCase):
    def setUp(self):
        user = User.objects.create(
            email="cokejnr@gmail.com",
            first_name="coke",
            last_name="jnr",
            password="12345",
        )

        image = SimpleUploadedFile(
            name="test_image.png",
            content=open(config("IMG_PATH"), mode="rb").read(),
            content_type="image/png",
        )

        self.order = Order.objects.create(
            owner=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone="+2348578853857307",
            address1="mushin",
            postal_code="1212",
            city="lagos",
        )

        product1 = Product.objects.create(
            name="Air jordan 1",
            price=500,
            image=image,
            description="literally one of the most wanted sneaker in the jordan",
            count_instock=8,
        )
        product2 = Product.objects.create(
            name="Adidas samba",
            price=200,
            image=image,
            description="The samba is one of the fastest selling products of adidas",
            count_instock=3,
        )

        order_item1 = OrderItem.objects.create(
            product=product1, order=self.order, qty=2
        )
        order_item2 = OrderItem.objects.create(
            product=product2, order=self.order, qty=2
        )

    def test_total_cost(self):
        self.assertEqual(self.order.get_total_cost(), 1400)


class TestOrderItemModel(TestCase):
    pass
