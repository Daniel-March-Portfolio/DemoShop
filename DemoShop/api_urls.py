from django.urls import path, include

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('categories/', include('Category.api_urls')),
    path('items/', include('Item.api_urls')),
    path('carts/', include('Cart.api_urls')),
]
