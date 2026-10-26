from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], min_length=12)
    password_confirm = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=[("customer","Customer"),("seller","Seller")], default="customer", write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password", "password_confirm", "role"]
        extra_kwargs = {"email": {"required": True}}
    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("এই ইমেইল দিয়ে অ্যাকাউন্ট আছে।")
        return value
    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password_confirm": "পাসওয়ার্ড দুটি মেলেনি।"})
        return attrs
    def create(self, validated_data):
        role = validated_data.pop("role", "customer")
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        profile = user.profile
        profile.role = role
        profile.save(update_fields=["role"])
        return user

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source="profile.role", read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role"]
