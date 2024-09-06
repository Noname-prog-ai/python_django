from timeit import default_timer
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView
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
    template_name = 'product_detail.html'
    context_object_name = 'product'

# Продукт Create View
class ProductCreateView(View):
    def get(self, request: HttpRequest):
        form = ProductForm()
        return render(request, 'shopapp/product_form.html', {'form': form})

    def post(self, request: HttpRequest):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products_list')
        return render(request, 'shopapp/product_form.html', {'form': form})

# Продукт Update View
class ProductUpdateView(View):
    def get(self, request: HttpRequest, pk: int):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(instance=product)
        return render(request, 'shopapp/product_form.html', {'form': form})

    def post(self, request: HttpRequest, pk: int):
        product = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
        return render(request, 'shopapp/product_form.html', {'form': form})

# Продукт Delete View
class ProductDeleteView(View):
    def get(self, request: HttpRequest, pk: int):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'shopapp/product_confirm_delete.html', {'product': product})

    def post(self, request: HttpRequest, pk: int):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return redirect('products_list')


# Заказ Details View
class OrderDetailsView(View):
    def get(self, request: HttpRequest, pk: int):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'shopapp/order_detail.html', {'order': order})

# Заказ Create View
class OrderCreateView(View):
    def get(self, request: HttpRequest):
        form = OrderForm()
        return render(request, 'shopapp/order_form.html', {'form': form})

    def post(self, request: HttpRequest):
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('orders_list')
        return render(request, 'shopapp/order_form.html', {'form': form})

# Заказ Update View
class OrderUpdateView(View):
    def get(self, request: HttpRequest, pk: int):
        order = get_object_or_404(Order, pk=pk)
        form = OrderForm(instance=order)
        return render(request, 'shopapp/order_form.html', {'form': form})

    def post(self, request: HttpRequest, pk: int):
        order = get_object_or_404(Order, pk=pk)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders_list')
        return render(request, 'shopapp/order_form.html', {'form': form})

# Заказ Delete View
class OrderDeleteView(View):
    def get(self, request: HttpRequest, pk: int):
        order = get_object_or_404(Order, pk=pk)
        return render(request, 'shopapp/order_confirm_delete.html', {'order': order})

    def post(self, request: HttpRequest, pk: int):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return redirect('orders_list')
