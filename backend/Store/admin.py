from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class HeroAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'id']
    search_fields = ['title']
    ordering = ['created']
admin.site.register(HeroSection, HeroAdmin)

class ProductImageInline (admin.TabularInline):
    model = ProductImage
    raw_id_fields = ['product']


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'old_price', 'category', 'audience', 'size', 'stock', 'available', 'created', 'updated']
    search_fields = ['name']
    ordering = ['created']
    inlines = [ProductImageInline]
admin.site.register(Product, ProductAdmin)



class CartItemInline (admin.TabularInline):
    model = CartItem
    raw_id_fields = ['cart']

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_code', 'id']
    search_fields = ['id']
    ordering = ['created']
    inlines = [CartItemInline]
admin.site.register(Cart, CartAdmin)

class RecentItemInline (admin.TabularInline):
    model = RecentItem
    raw_id_fields = ['recent']
    ordering = ['-created']

class RecentAdmin(admin.ModelAdmin):
    list_display = ['recent_code', 'id']
    search_fields = ['id']
    ordering = ['created']     
    inlines = [RecentItemInline]
admin.site.register(Recent, RecentAdmin)


admin.site.register(AudienceType)
admin.site.register(Category)
admin.site.register(Order)