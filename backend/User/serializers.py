from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model


class UserSerializer (serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'state', 'country', 'city_or_town', 'local_government', 'nearest_bus_stop', 'house_address', 'date_joined', 'password']
        