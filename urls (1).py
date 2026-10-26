from django.urls import path
from .views import RegisterView, login_view, logout_view, me_view, csrf_view, password_reset_request, password_reset_confirm
urlpatterns = [
    path("csrf/", csrf_view, name="csrf"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("me/", me_view, name="me"),
    path("password-reset/request/", password_reset_request, name="password-reset-request"),
    path("password-reset/confirm/", password_reset_confirm, name="password-reset-confirm"),
]
