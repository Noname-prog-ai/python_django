from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Order, Product
from django.contrib.auth.models import Permission

User = get_user_model()

class OrderDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание пользователя с правами просмотра заказа
        cls.user = User.objects.create_user(username='testuser', password='testpassword', is_staff=True)
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

        # Создание продуктов для тестов
        cls.product = Product.objects.create(name='Test Product')

    def setUp(self):
        # Вход пользователя
        self.client.login(username='testuser', password='testpassword')

        # Создание заказа после входа
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='Test Address',
            promocode='TESTCODE',
        )
        self.order.products.add(self.product)  # Добавляем продукт к заказу

    def tearDown(self):
        # Удаление заказа
        self.order.delete()

    def test_order_detail_view(self):
        response = self.client.get(reverse('shopapp:order_details', args=[self.order.pk]))

        # Проверка статуса ответа
        self.assertEqual(response.status_code, 200)
        # Проверка содержимого ответа
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание пользователя с правами
        cls.user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

        # Создание продуктов
        cls.product1 = Product.objects.create(name='Product 1')
        cls.product2 = Product.objects.create(name='Product 2')

        # Создание заказов и связывание с продуктами
        cls.order1 = Order.objects.create(user=cls.user, delivery_address='Address 1', promocode='CODE1')
        cls.order1.products.add(cls.product1)
        cls.order2 = Order.objects.create(user=cls.user, delivery_address='Address 2', promocode='CODE2')
        cls.order2.products.add(cls.product2)

    def setUp(self):
        # Вход пользователя с правами
        self.client.login(username='staffuser', password='staffpassword')

    def tearDown(self):
        # Удаление заказов
        self.order1.delete()
        self.order2.delete()
        # Удаление пользователя и продуктов
        self.product1.delete()
        self.product2.delete()
        self.user.delete()

    def test_orders_export_view(self):
        response = self.client.get(reverse('shopapp:orders_export'))

        # Проверка статуса ответа
        self.assertEqual(response.status_code, 200)

        # Получение всех заказов
        orders = Order.objects.select_related('user').prefetch_related('products').all()

        # Проверка структуры ответа
        expected_data = [
            {
                'id': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user.pk,
                'product_ids': [product.pk for product in order.products.all()]
            }
            for order in orders
        ]

        self.assertJSONEqual(response.content, expected_data)
