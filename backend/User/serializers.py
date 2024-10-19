from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone_number', 'state', 'country',
            'city_or_town', 'local_government',
            'nearest_bus_stop', 'house_address', 'date_joined', 'password'
        ]
        extra_kwargs = {
            'date_joined': {'read_only': True}, 
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],  # Ensure email is provided
            password=validated_data.pop('password'),  # Get and remove password
            **validated_data  # Pass remaining fields to create_user
        )
        return user

    def validate_email(self, value):
        # Optionally add email validation
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
