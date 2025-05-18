from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, ChangePasswordSerializer, UserDetailSerializer # Added UserDetailSerializer
from .permissions import IsAuthenticatedAndActive
from .models import CustomUser, TeacherProfile, StudentProfile # Import the profile models
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        # Create profile based on role.  This is the most important change.
        if user.role == 'TEACHER':
            TeacherProfile.objects.create(user=user)
        elif user.role == 'STUDENT':
            StudentProfile.objects.create(user=user)

        user.is_verified = True # Bypass email verification.
        user.save()
        logger.info(f"User {user.email} registered as {user.role} successfully.")

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        logger.info(f"User {user.email} logged in successfully.")
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        logger.warning(f"Login failed for email: {email}")
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer # Use the new serializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() # simplify

        return Response({'detail': 'User profile updated successfully'}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticatedAndActive]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        old_password = serializer.validated_data['old_password']
        if not user.check_password(old_password):
            return Response({'old_password': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Password changed successfully'}, status=status.HTTP_200_OK)