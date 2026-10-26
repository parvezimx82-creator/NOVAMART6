import uuid
from django.conf import settings
from django.db import models

class PaymentMethod(models.Model):
    class Category(models.TextChoices):
        MOBILE_BANKING = "mobile_banking", "Mobile banking"
        CARD = "card", "Card"
        CRYPTO = "crypto", "Cryptocurrency"
        CASH = "cash", "Cash on delivery"
        OTHER = "other", "Other"

    code = models.SlugField(max_length=40, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=24, choices=Category.choices)
    description = models.CharField(max_length=240, blank=True)
    instructions = models.TextField(blank=True, help_text="Shown to customers for manual payment methods.")
    network = models.CharField(max_length=80, blank=True, help_text="For example: TRC20, BEP20, BCH network.")
    recipient_details = models.CharField(max_length=180, blank=True, help_text="Public wallet address or merchant number only. Never store secret keys.")
    is_active = models.BooleanField(default=False)
    is_manual = models.BooleanField(default=True, help_text="Manual methods require admin verification.")
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} ({'active' if self.is_active else 'inactive'})"


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending verification"
        PROCESSING = "processing", "Processing"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    reference = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    order = models.ForeignKey("orders.Order", on_delete=models.PROTECT, related_name="payments")
    method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name="payments")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=8, default="BDT")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    customer_transaction_id = models.CharField(max_length=160, blank=True)
    provider_reference = models.CharField(max_length=180, blank=True)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status", "created_at"]), models.Index(fields=["customer", "created_at"])]

    def __str__(self):
        return f"Payment {self.reference} — {self.status}"
