from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

User = get_user_model()

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # No need to pass commit=False
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save()  # Save the user directly
        # user.set_password(user.password)
        user.save()  # Save the user with the hashed password



class GetUserView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        user = self.request.user
        return User.objects.get(id=user.id)
    

class UpdateUserProfile(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return User.objects.get(id=user.id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)  # Allow partial updates
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    

class VerifyEmailView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            # Generate a password reset token
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)

            # Encode the user ID
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create the reset password URL (you would replace this with your frontend URL)
            reset_url = f"{settings.FRONTEND_URL}/resetpassword/{uid}/{token}"

            # Send the email
            send_mail(
                subject="Password Reset Request",
                message=f"Hi {user.first_name} {user.last_name},\n\nClick the link below to reset your password:\n{reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent to your email."}, status=200)
        else:
            return Response({"error": "User with this email does not exist."}, status=404)



class SetNewPasswordView(APIView):
    def put(self, request, uid, token, *args, **kwargs):
        # Decode the user ID from the uidb64 parameter
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid token or user ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the reset token
        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired reset token"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the password and confirm_password from request data
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the new password is the same as the old one
        if user.check_password(password):
            return Response({"error": "You have already used this password before"}, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(password)
        user.save()

        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_202_ACCEPTED)
    
    
        

