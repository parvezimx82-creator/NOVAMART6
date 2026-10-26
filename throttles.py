from rest_framework.throttling import AnonRateThrottle
class LoginThrottle(AnonRateThrottle):
    scope = "auth"
class RegisterThrottle(AnonRateThrottle):
    scope = "register"
class PasswordResetThrottle(AnonRateThrottle):
    scope = "password_reset"
