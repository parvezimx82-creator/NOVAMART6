from django.contrib import admin, messages
from django.db import transaction
from .models import PaymentMethod, Payment

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "category", "network", "is_active", "is_manual", "display_order")
    list_filter = ("category", "is_active", "is_manual")
    search_fields = ("name", "code", "network", "recipient_details")
    fieldsets = (
        ("পদ্ধতির পরিচিতি", {"fields": ("name", "code", "category", "description", "display_order")}),
        ("গ্রাহকের পেমেন্ট নির্দেশনা", {"fields": ("instructions", "network", "recipient_details")}),
        ("সক্রিয়করণ ও যাচাই", {"fields": ("is_active", "is_manual")}),
    )
    actions = ["disable_selected_methods"]

    @admin.action(description="নির্বাচিত পেমেন্ট পদ্ধতি বন্ধ করুন")
    def disable_selected_methods(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count}টি পেমেন্ট পদ্ধতি বন্ধ করা হয়েছে।")
    list_editable = ("is_active", "display_order")

@admin.action(description="Mark selected payments as verified/paid")
def mark_paid(modeladmin, request, queryset):
    changed = 0
    for payment in queryset.select_related("order"):
        with transaction.atomic():
            payment = Payment.objects.select_for_update().get(pk=payment.pk)
            if payment.status in [Payment.Status.PENDING, Payment.Status.PROCESSING]:
                payment.status = Payment.Status.PAID
                payment.save(update_fields=["status", "updated_at"])
                changed += 1
    modeladmin.message_user(request, f"{changed} payment(s) marked paid. Confirm funds independently before using this action.", messages.WARNING)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("reference", "order", "customer", "method", "amount", "currency", "status", "created_at")
    list_per_page = 50
    list_filter = ("status", "method", "currency", "created_at")
    search_fields = ("reference", "customer_transaction_id", "provider_reference", "order__id")
    readonly_fields = ("reference", "created_at", "updated_at")
    actions = [mark_paid]
