from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure the password is write-only

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'state',
            'country',
            'city_or_town',
            'local_government',
            'nearest_bus_stop',
            'house_address',
            'date_joined',
            'password'  # Include password for user creation
        ]

    def create(self, validated_data):
        user = User(**validated_data)  # Create user instance without saving
        user.set_password(validated_data['password'])  # Hash the password
        user.save()  # Save the user with hashed password
        return user
