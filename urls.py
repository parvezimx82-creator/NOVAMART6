from django.urls import path
from . import views

urlpatterns = [
    path("methods/", views.payment_methods, name="payment-methods"),
    path("submit/", views.submit_payment, name="submit-payment"),
    path("mine/", views.my_payments, name="my-payments"),
]
