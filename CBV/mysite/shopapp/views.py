from timeit import default_timer
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product, Order
from .forms import ProductForm, OrderForm


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


# Продукт Details View
class ProductDetailsView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'
    context_object_name = 'product'


# Продукт Create View
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'

    def form_valid(self, form):
        return super().form_valid(form)


# Продукт Update View
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shopapp/product_form.html'


# Продукт Delete View
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'shopapp/product_confirm_delete.html'
    success_url = '/products/'

# Заказ Details View
class OrderDetailsView(DetailView):
    model = Order
    template_name = 'shopapp/order_detail.html'
    context_object_name = 'order'


# Заказ Create View
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/order_form.html'


# Заказ Update View
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'shopapp/order_form.html'


# Заказ Delete View
class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'shopapp/order_confirm_delete.html'
    success_url = '/orders/'