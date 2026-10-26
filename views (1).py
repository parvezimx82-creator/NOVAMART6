from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.middleware.csrf import get_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from .throttles import LoginThrottle, RegisterThrottle, PasswordResetThrottle

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [RegisterThrottle]

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def csrf_view(request):
    return Response({"csrfToken": get_token(request)})

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@throttle_classes([LoginThrottle])
def login_view(request):
    username = (request.data.get("username") or "").strip()
    password = request.data.get("password") or ""
    user = authenticate(request, username=username, password=password)
    if user is None:
        return Response({"detail": "লগইন তথ্য সঠিক নয়।"}, status=status.HTTP_400_BAD_REQUEST)
    login(request, user)
    return Response({"user": UserSerializer(user).data, "detail": "লগইন সফল হয়েছে।"})

@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"detail": "লগআউট হয়েছে।"})

@api_view(["GET"])
def me_view(request):
    if not request.user.is_authenticated:
        return Response({"authenticated": False}, status=200)
    return Response({"authenticated": True, "user": UserSerializer(request.user).data})

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@throttle_classes([PasswordResetThrottle])
def password_reset_request(request):
    email = (request.data.get("email") or "").strip().lower()
    # Identical response prevents account enumeration.
    generic = {"detail": "ইমেইলটি অ্যাকাউন্টে থাকলে রিসেট নির্দেশনা পাঠানো হবে।"}
    if email:
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            # In production, configure a real transactional email provider and frontend URL.
            reset_url = f"{getattr(settings, 'FRONTEND_BASE_URL', 'http://localhost:3000')}/reset-password?uid={uid}&token={token}"
            send_mail("NOVAMART password reset", f"পাসওয়ার্ড রিসেট করতে এই লিংক খুলুন: {reset_url}", None, [user.email], fail_silently=True)
    return Response(generic)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
@throttle_classes([PasswordResetThrottle])
def password_reset_confirm(request):
    uid = request.data.get("uid") or ""
    token = request.data.get("token") or ""
    password = request.data.get("password") or ""
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id, is_active=True)
    except Exception:
        return Response({"detail":"রিসেট লিংকটি সঠিক নয় বা মেয়াদ শেষ হয়েছে।"}, status=400)
    if not default_token_generator.check_token(user, token):
        return Response({"detail":"রিসেট লিংকটি সঠিক নয় বা মেয়াদ শেষ হয়েছে।"}, status=400)
    try:
        validate_password(password, user)
    except Exception as e:
        return Response({"detail": str(e)}, status=400)
    user.set_password(password)
    user.save(update_fields=["password"])
    return Response({"detail":"পাসওয়ার্ড পরিবর্তন হয়েছে। এখন নতুন পাসওয়ার্ড দিয়ে লগইন করুন।"})
