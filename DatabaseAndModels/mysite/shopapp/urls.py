from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_index, name='shop_index'),
    path('products/', views.product_list, name='product_list'),
    path('orders/', views.order_list, name='order_list'),
]