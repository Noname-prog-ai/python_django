from django.urls import path
from .views import (
    ShopIndexView,
    GroupsListView,
    ProductsListView,
    OrdersListView,
    ProductDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderDetailsView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
)

urlpatterns = [
    path('', ShopIndexView.as_view(), name='shop_index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_detail'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='order_detail'),
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/edit/', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order_delete'),
]
