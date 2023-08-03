from django.urls import path,include
from shop.views import index,detail
from . import views

urlpatterns = [
    path('', index, name='Home'),
    path('<int:myid>', detail, name='Detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('accounts/', include('django.contrib.auth.urls')),
]