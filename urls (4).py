from django.urls import path
from .views import MyOrdersView, create_order

urlpatterns = [
    path("mine/", MyOrdersView.as_view(), name="my-orders"),
    path("create/", create_order, name="create-order"),
]
