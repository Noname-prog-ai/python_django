from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Product
from django.http import HttpResponseRedirect


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(is_archived=False)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('product_list')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('product_list')


class ProductArchiveView(TemplateView):
    template_name = 'products/product_archive_confirm.html'

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(pk=self.kwargs['pk'])
        product.is_archived = True
        product.save()
        return HttpResponseRedirect(reverse_lazy('product_list'))