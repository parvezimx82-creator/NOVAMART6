from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health(_request):
    return JsonResponse({"status": "ok", "service": "NOVAMART API"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health),
    path("api/auth/", include("accounts.urls")),
    path("api/catalog/", include("catalog.urls")),
    path("api/orders/", include("orders.urls")),
    path("api/payments/", include("payments.urls")),
    path("api/chat/", include("livechat.urls")),
]
