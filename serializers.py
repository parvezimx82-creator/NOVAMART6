from rest_framework import serializers
from .models import PaymentMethod, Payment

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["code", "name", "category", "description", "instructions", "network", "recipient_details", "is_manual", "is_active"]

class PaymentSerializer(serializers.ModelSerializer):
    method_name = serializers.CharField(source="method.name", read_only=True)
    class Meta:
        model = Payment
        fields = ["reference", "order", "method_name", "amount", "currency", "status", "customer_transaction_id", "created_at"]
        read_only_fields = ["reference", "amount", "currency", "status", "created_at", "method_name"]
