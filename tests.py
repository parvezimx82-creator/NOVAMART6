from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from catalog.models import Category, Product
from payments.models import PaymentMethod, Payment
from .models import Order

class OrderCreationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = User.objects.create_user(username="buyer_test", password="StrongPassphrase!123")
        self.seller = User.objects.create_user(username="seller_test", password="StrongPassphrase!123")
        self.category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            seller=self.seller, category=self.category, name="Test product",
            slug="test-product", price=Decimal("125.00"), stock=5,
            status=Product.Status.ACTIVE,
        )
        PaymentMethod.objects.create(
            code="cod", name="Cash on Delivery", category=PaymentMethod.Category.CASH,
            is_active=True, is_manual=True,
        )
        PaymentMethod.objects.create(
            code="bkash", name="bKash", category=PaymentMethod.Category.MOBILE_BANKING,
            is_active=True, is_manual=True,
        )
        self.client.force_authenticate(self.customer)

    def test_order_uses_server_price_and_decrements_stock(self):
        response = self.client.post("/api/orders/create/", {
            "customer_name": "Buyer", "phone": "01700000000", "address": "Dhaka",
            "items": [{"product_id": self.product.id, "quantity": 2, "price": "1.00"}],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(order.total, Decimal("250.00"))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_insufficient_stock_rejected(self):
        response = self.client.post("/api/orders/create/", {
            "customer_name": "Buyer", "phone": "01700000000", "address": "Dhaka",
            "items": [{"product_id": self.product.id, "quantity": 6}],
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_manual_payment_requires_reference_before_order_is_created(self):
        response = self.client.post("/api/orders/create/", {
            "customer_name": "Buyer", "phone": "01700000000", "address": "Dhaka",
            "payment_method": "bkash",
            "items": [{"product_id": self.product.id, "quantity": 1}],
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)

    def test_cash_on_delivery_order_is_created(self):
        response = self.client.post("/api/orders/create/", {
            "customer_name": "Buyer", "phone": "01700000000", "address": "Dhaka",
            "payment_method": "cod",
            "items": [{"product_id": self.product.id, "quantity": 1}],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["payment_status"], "cash_on_delivery")
        self.assertEqual(Payment.objects.count(), 0)
