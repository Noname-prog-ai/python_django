from django.urls import path

from .views import ShopIndexView, GroupsListView, ProductsListView, OrdersListView

app_name = "shopapp"

urlpatterns = [
    path('', ShopIndexView.as_view(), name='shop_index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
]
