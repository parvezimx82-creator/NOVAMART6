from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from orders.models import Order
from .models import PaymentMethod, Payment
from .serializers import PaymentMethodSerializer, PaymentSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def payment_methods(request):
    methods = PaymentMethod.objects.all()
    return Response(PaymentMethodSerializer(methods, many=True).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def submit_payment(request):
    order_id = request.data.get("order")
    method_code = request.data.get("method")
    transaction_id = str(request.data.get("transaction_id", "")).strip()[:160]
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    method = get_object_or_404(PaymentMethod, code=method_code, is_active=True)
    if order.status in [Order.Status.CANCELLED, Order.Status.REFUNDED]:
        return Response({"detail": "This order cannot be paid."}, status=status.HTTP_400_BAD_REQUEST)
    if method.is_manual and not transaction_id and method.category != PaymentMethod.Category.CASH:
        return Response({"detail": "Enter the transaction/reference ID to request manual verification."}, status=status.HTTP_400_BAD_REQUEST)
    payment = Payment.objects.create(
        order=order, method=method, customer=request.user, amount=order.total,
        currency="BDT", customer_transaction_id=transaction_id,
        status=Payment.Status.PENDING if method.is_manual else Payment.Status.PROCESSING,
    )
    return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_payments(request):
    return Response(PaymentSerializer(Payment.objects.filter(customer=request.user)[:100], many=True).data)
