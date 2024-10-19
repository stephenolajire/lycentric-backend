from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Make the password write-only

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone_number', 'state', 'country',
            'city_or_town', 'local_government',
            'nearest_bus_stop', 'house_address', 
            'date_joined', 'password'
        ]
    
        def create(self, validated_data):
            password = validated_data.pop('password')  # Extract the password
            user = User(**validated_data)  # Create user without password for now
            user.set_password(password)  # Hash the password
            user.save()  # Save the user with hashed password
            return user
