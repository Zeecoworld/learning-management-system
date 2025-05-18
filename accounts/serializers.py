from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAuthenticatedAndActive
from .models import CustomUser, TeacherProfile, StudentProfile 
import logging
from rest_framework import serializers 

# Get an instance of a logger
logger = logging.getLogger(__name__)



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'role') 
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'] #added role here
        )
        return user



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"new_password": "Passwords must match"})
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is incorrect"})
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = '__all__'
        # exclude = ('user',) # Important: Do not include the user field to avoid circular references

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        # exclude = ('user',)  # Important: Do not include the user field to avoid circular references


class UserDetailSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(read_only=True)  #  Use correct related names
    student_profile = StudentProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'role', 'first_name', 'last_name', 'phone_number', 'address', 'employee_id',
                  'department', 'bio', 'hire_date', 'qualification', 'student_id', 'enrollment_date',
                  'graduation_date', 'major', 'teacher_profile', 'student_profile']  # Include all relevant fields
        read_only_fields = ['email', 'role'] # Prevent these from being changed.