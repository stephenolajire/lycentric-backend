from django.db import models
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

class AudienceType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)  # e.g., 'Male', 'Female', 'Kid'
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='category', default="../image.png")
   
    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    audience = models.ForeignKey(AudienceType, related_name='age', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='group', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created']


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Image"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart_code = models.CharField(max_length=100, blank=False, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_code


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.cart.cart_code}"

    def total_price(self):
        return self.quantity * self.product.price

    

class HeroSection (models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    image = models.ImageField(upload_to='Hero')
    title = models.CharField(max_length=300)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Recent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recent_code = models.CharField(max_length=100, blank=False, null=False, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recent_code


class RecentItem(models.Model):
    recent = models.ForeignKey(Recent, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='recent_items', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-created']
    

class Order (models.Model):
    firstName = models.CharField (max_length=200)
    lastName = models.CharField (max_length=200)
    phoneNumber = models.CharField (max_length=20)
    email = models. EmailField ()
    state = models.CharField (max_length=200)
    city = models.CharField (max_length=200)
    localGovernment = models.CharField (max_length=300)
    nearestBusStop = models.CharField (max_length=500)
    homeAddress = models.CharField (max_length=1000)
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    cart = models.ForeignKey (Cart, on_delete=models.CASCADE)
    items = models.ForeignKey (CartItem, on_delete=models.CASCADE)
    amount = models.FloatField ()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstName

    class Meta:
        ordering = ['-created']