from decimal import Decimal
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from catalog.models import Product
from payments.models import Payment, PaymentMethod
from .models import Order, OrderItem
from .serializers import OrderSerializer


class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).prefetch_related("items")


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
@throttle_classes([UserRateThrottle])
def create_order(request):
    items = request.data.get("items")
    name = str(request.data.get("customer_name", "")).strip()[:150]
    phone = str(request.data.get("phone", "")).strip()[:30]
    address = str(request.data.get("address", "")).strip()[:1500]
    method_code = str(request.data.get("payment_method", "cod")).strip()[:40] or "cod"
    transaction_id = str(request.data.get("transaction_id", "")).strip()[:160]

    if not isinstance(items, list) or not items or len(items) > 50:
        return Response({"detail": "কার্টে ১ থেকে ৫০টি পণ্যের লাইন থাকতে হবে।"}, status=status.HTTP_400_BAD_REQUEST)
    if not name or not phone or len(phone) < 7 or not address:
        return Response({"detail": "নাম, সঠিক ফোন নম্বর ও ডেলিভারি ঠিকানা দিন।"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        method = PaymentMethod.objects.get(code=method_code, is_active=True)
    except PaymentMethod.DoesNotExist:
        return Response({"detail": "নির্বাচিত পেমেন্ট পদ্ধতি বর্তমানে চালু নেই।"}, status=status.HTTP_400_BAD_REQUEST)

    if method.category != PaymentMethod.Category.CASH and method.is_manual and not transaction_id:
        return Response({"detail": "ম্যানুয়াল পেমেন্টের লেনদেন/রেফারেন্স আইডি দিন।"}, status=status.HTTP_400_BAD_REQUEST)

    normalized = {}
    try:
        for item in items:
            product_id = int(item.get("product_id"))
            quantity = int(item.get("quantity"))
            if product_id <= 0 or quantity < 1 or quantity > 99:
                raise ValueError
            normalized[product_id] = normalized.get(product_id, 0) + quantity
        if any(qty > 99 for qty in normalized.values()):
            raise ValueError
    except (AttributeError, TypeError, ValueError):
        return Response({"detail": "পণ্যের আইডি বা পরিমাণ সঠিক নয়।"}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        locked_products = list(
            Product.objects.select_for_update()
            .filter(id__in=normalized.keys(), status=Product.Status.ACTIVE)
            .select_related("seller")
        )
        by_id = {p.id: p for p in locked_products}
        if len(by_id) != len(normalized):
            return Response({"detail": "কিছু পণ্য আর উপলভ্য নেই। কার্ট আপডেট করুন।"}, status=status.HTTP_400_BAD_REQUEST)
        for product_id, qty in normalized.items():
            if by_id[product_id].stock < qty:
                return Response({"detail": f"{by_id[product_id].name} পণ্যের পর্যাপ্ত স্টক নেই।"}, status=status.HTTP_400_BAD_REQUEST)

        subtotal = sum((by_id[pid].price * qty for pid, qty in normalized.items()), Decimal("0.00"))
        shipping_fee = Decimal("0.00")  # Configure shipping policy before production.
        order = Order.objects.create(
            customer=request.user, subtotal=subtotal, shipping_fee=shipping_fee,
            total=subtotal + shipping_fee, customer_name=name, phone=phone, address=address,
        )
        for product_id, qty in normalized.items():
            product = by_id[product_id]
            OrderItem.objects.create(
                order=order, product=product, seller=product.seller,
                product_name=product.name, unit_price=product.price, quantity=qty,
            )
            product.stock -= qty
            product.save(update_fields=["stock"])

        if method.category != PaymentMethod.Category.CASH:
            Payment.objects.create(
                order=order, method=method, customer=request.user,
                amount=order.total, currency="BDT",
                customer_transaction_id=transaction_id,
                status=Payment.Status.PENDING if method.is_manual else Payment.Status.PROCESSING,
            )

    data = OrderSerializer(order).data
    data["payment_status"] = (
        "cash_on_delivery" if method.category == PaymentMethod.Category.CASH
        else "pending_verification" if method.is_manual
        else "processing"
    )
    return Response(data, status=status.HTTP_201_CREATED)
