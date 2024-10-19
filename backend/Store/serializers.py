from rest_framework import serializers
from .models import *


class HeroSerializer (serializers.ModelSerializer):
  class Meta:
    model = HeroSection
    fields = ['id', 'title', 'description', 'image']


class CategorySerializer (serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id', 'name', 'image']

class AudienceSerializer (serializers.ModelSerializer):
  class Meta:
    model = AudienceType
    fields = ['id', 'name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'old_price', 'category', 'audience', 'size', 'stock', 'available', 'created', 'updated', 'images']
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) 
    total_price = serializers.SerializerMethodField()  # Calculating total price for the cart item

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']  # Include the necessary fields

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)  # Display all items in the cart
    total_cart_price = serializers.SerializerMethodField()  # Total price of the cart
    total_quantity = serializers.SerializerMethodField()  # Total quantity of all items in the cart

    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'items', 'total_cart_price', 'total_quantity']  # Include the necessary fields

    def get_total_cart_price(self, obj):
        # Sum up the total price of each cart item
        return sum(item.quantity * item.product.price for item in obj.items.all())

    def get_total_quantity(self, obj):
        # Sum up the quantity of each cart item
        return sum(item.quantity for item in obj.items.all())
    

class RecentItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Calculating total price for the cart item

    class Meta:
        model = RecentItem
        fields = ['id', 'product']  # Include the necessary fields
    

class RecentSerializer(serializers.ModelSerializer):
    items = RecentItemSerializer(many=True, read_only=True)  # Display all items in the cart

    class Meta:
        model = Recent
        fields = ['id', 'recent_code', 'items'] 


class OrderSerializer(serializers.ModelSerializer):
    # To represent the `User`, `Cart`, and `CartItem` as nested serializers.
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Reference to the User model
    cart = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all())  # Reference to the Cart model
    items = serializers.PrimaryKeyRelatedField(queryset=CartItem.objects.all())  # Reference to the CartItem model

    class Meta:
        model = Order
        fields = ['id', 'firstName', 'lastName', 'phoneNumber', 'email', 'state', 'city', 'localGovernment', 'nearestBusStop', 'homeAddress', 'user', 'cart', 'items', 'amount', 'created']
        read_only_fields = ['created']