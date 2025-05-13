from timeit import default_timer

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.test import TestCase

from .models import Product, Order

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
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

class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    model = Product
    context_object_name = "product"

class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)

class ProductCreateView(CreateView):
    model = Product
    fields = "name", "price", "description", "discount"
    success_url = reverse_lazy("shopapp:products_list")

class ProductUpdateView(UpdateView):
    model = Product
    fields = "name", "price", "description", "discount"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "shopapp:product_details",
            kwargs={"pk": self.object.pk},
        )

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class OrdersListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.select_related("user").prefetch_related("products")
        orders_data = [
            {
                "pk": order.pk,
                "promocode": order.promocode,
                "delivery_address": order.delivery_address,
                "user_pk": order.user.pk,
                "products": [p.pk for p in order.products.all()],
            }
            for order in orders
        ]
        return JsonResponse({"orders": orders_data})


class OrdersExportTestCase(TestCase):
    fixtures = [
        "users-fixture.json",
        # и остальные файлы
    ]

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            is_active=True,
            is_staff=True,
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_export_orders(self):
        response = self.client.get(reverse("shopapp:orders_export"))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        # Делаем запрос и составляем список
        orders = Order.objects.select_related("user").prefetch_related("products")
        orders_data = [
            {
                "pk": order.pk,
                "promocode": order.promocode,
                "delivery_address": order.delivery_address,
                "user_pk": order.user.pk,
                "products": [p.pk for p in order.products.all()],
            }
            for order in orders
        ]

        # Сравниваем
        self.assertEqual(
            response_data["orders"],
            orders_data,
        )