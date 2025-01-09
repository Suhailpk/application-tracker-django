from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, OTP
from .serializers import ChangePasswordSerializer, OtpRequestSerializer, OTPVerifySerailizer
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.viewsets import ViewSet



class OTPRequestViewset(ViewSet):
    permission_classes = []

    def create(self, request):
        """
        Handles POST requests for creating and sending OTPs.
        """
        serializer = OtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.create_otp()

            # Send email
            send_mail(
                subject="Please verify with OTP code",
                message=f"Your OTP code is {otp.otp_code}",
                from_email="suhailpk2427@gmail.com",
                recipient_list=[otp.email],
            )
            return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OTPVerifyViewSet(ViewSet):
    permission_classes = []

    def create(self, request):
        """
        Handles POST requests for verifying OTPs.
        """
        serializer = OTPVerifySerailizer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp']
            try:
                otp = OTP.objects.get(otp_code=otp_code, is_verified=False)
                
                # Check OTP expiry
                if otp.created_at + timedelta(minutes=5) < now():
                    return Response(request,{"error": "OTP expired."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Mark OTP as verified
                otp.is_verified = True
                otp.save()
                return Response({"message": "OTP verified successfully!"}, status=status.HTTP_200_OK)
            
            except OTP.DoesNotExist:
                return Response(request,{"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordViewSet(ViewSet):
    permission_classes = []

    def create(self, request):
        """
        Handles POST requests for changing passwords.
        """
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password updated successfully!"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

