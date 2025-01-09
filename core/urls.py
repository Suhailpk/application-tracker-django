from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ChangePasswordViewSet, OTPRequestViewset, OTPVerifyViewSet


router = DefaultRouter()
router.register(r'otp-request', OTPRequestViewset, basename='otp-request')
router.register(r'otp-verify', OTPVerifyViewSet, basename='otp-verify')
router.register(r'change-password', ChangePasswordViewSet, basename='change-password')


urlpatterns = [
    path('', include(router.urls)),
]