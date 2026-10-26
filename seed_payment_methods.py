from django.core.management.base import BaseCommand
from payments.models import PaymentMethod

METHODS = [
    ("cod", "Cash on Delivery", "cash", "Pay cash when your order arrives.", "", "", True, True, 1),
    ("bkash", "bKash", "mobile_banking", "Bangladesh mobile financial service; enable only after merchant setup.", "", "", False, True, 10),
    ("nagad", "Nagad", "mobile_banking", "Bangladesh mobile financial service; enable only after merchant setup.", "", "", False, True, 11),
    ("rocket", "Rocket", "mobile_banking", "Dutch-Bangla Bank mobile financial service; enable only after merchant setup.", "", "", False, True, 12),
    ("upay", "upay", "mobile_banking", "Bangladesh mobile financial service; enable only after merchant setup.", "", "", False, True, 13),
    ("card", "Visa Card", "card", "Enable only after connecting an approved card payment gateway that supports Visa.", "", "", False, False, 20),
    ("usdt_bsc", "USDT (BSC / BEP20)", "crypto", "USDT transfer on BNB Smart Chain (BSC), commonly called BEP20. Manual verification until a blockchain/provider verifier is integrated.", "BSC (BEP20)", "", False, True, 30),
]

class Command(BaseCommand):
    help = "Create NOVAMART payment methods; legacy crypto options are disabled, not deleted, to preserve payment history."

    def handle(self, *args, **options):
        # Keep old records for historical orders, but make unsupported networks unavailable.
        PaymentMethod.objects.filter(code__in=["bch", "usdt_trc20", "usdt_bep20"]).update(is_active=False)
        for code, name, category, description, network, recipient, active, manual, order in METHODS:
            PaymentMethod.objects.update_or_create(
                code=code,
                defaults={
                    "name": name, "category": category, "description": description,
                    "network": network, "recipient_details": recipient,
                    "is_active": active, "is_manual": manual, "display_order": order,
                },
            )
        self.stdout.write(self.style.SUCCESS("Payment methods seeded. Only USDT on BSC (BEP20) is offered; configure providers before enabling live methods."))
