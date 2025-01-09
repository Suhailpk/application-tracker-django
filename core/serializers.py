from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import OTP
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth import get_user_model


User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')


from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Primary identifier
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registered")

    def validate(self, data):
        # Ensure new password matches confirmation
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"new_password": "Passwords do not match."})
        return data



class OtpRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("This email is not registered")



    def create_otp(self):
        email = self.validated_data['email']
        otp = OTP()
        otp.email = email
        otp.generate_otp()
        otp.save()
        return otp
    

class OTPVerifySerailizer(serializers.Serializer):
    otp = serializers.CharField()

    def validate_otp(self, value):
        try:
            otp_instance = OTP.objects.get(otp_code=value, is_verified=False)
            if otp_instance.created_at + timedelta(minutes=5) < now():
                raise serializers.ValidationError("OTP expired.")
            return value
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")

