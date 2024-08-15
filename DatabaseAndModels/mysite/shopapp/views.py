from django.shortcuts import render

# Create your views here.
from .models import Product, Order

def shop_index(request):
    return render(request, 'shopapp/index.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shopapp/products_list.html', {'products': products})


def order_list(request):
    orders = Order.objects.select_related('user').prefetch_related('products').all()
    return render(request, 'shopapp/orders_list.html', {'orders': orders})