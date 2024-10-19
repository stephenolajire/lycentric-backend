from django.urls import path
from . views import *

urlpatterns = [
  path ('hero/', HeroView.as_view()),
  path ('category/', CategoryView.as_view()),
  path ('audience/', AudienceView.as_view()),
  path ('allproduct/', AllProductsView.as_view()),
  path('category/<uuid:categoryId>/', CategoryItemView.as_view()),
  path('products/<uuid:categoryId>/<uuid:audienceId>/', CategoryAudienceView.as_view()),
  path('product/<uuid:id>/', ProductDetailView.as_view(), name='product-detail'),
  path ('cart/', AddToCartView.as_view()),
  path('cart/<str:cart_code>/', CartItemView.as_view(), name='cart-items'),
   path ('recentlyviewed/', AddToRecentlyView.as_view()),
  path('recent/<str:recent_code>/', RecentItemView.as_view(), name='cart-items'),
  path('api/cart/increment/', IncrementCartItemView.as_view(), name='increment_cart_item'),
  path('api/cart/decrement/', DecrementCartItemView.as_view(), name='decrement_cart_item'),
  path('api/cart/item/delete/', DeleteView.as_view(), name='delete_cart_item'),
  path('products/search/', ProductSearchView.as_view(), name='product-search'),
]