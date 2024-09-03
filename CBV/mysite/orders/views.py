from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .models import Order
from django.http import HttpResponseRedirect

class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'

class OrderCreateView(CreateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['user', 'products']
    success_url = reverse_lazy('order_list')

class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'orders/order_form.html'
    fields = ['user', 'products']
    success_url = reverse_lazy('order_list')

class OrderDeleteView(TemplateView):
    template_name = 'orders/order_delete_confirm.html'

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs['pk'])
        order.delete()
        return HttpResponseRedirect(reverse_lazy('order_list'))
