from timeit import default_timer
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Product, Order


class ShopIndexView(View):
    def get(self, request: HttpRequest):
        products = [
            ('Laptop', 1999),
            ('Desktop', 2999),
            ('Smartphone', 999),
        ]
        context = {
            "time_running": default_timer(),
            "products": products,
        }
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(ListView):
    model = Group
    template_name = 'shopapp/groups-list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return self.model.objects.prefetch_related('permissions').all()


class ProductsListView(ListView):
    model = Product
    template_name = 'shopapp/products-list.html'
    context_object_name = 'products'


class OrdersListView(ListView):
    model = Order
    template_name = 'shopapp/orders-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return self.model.objects.select_related("user").prefetch_related("products").all()