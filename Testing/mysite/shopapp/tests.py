from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Order, Product  # Импортируйте ваши модели

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

    fixtures = ['test_fixtures.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)

    def setUp(self):
        self.client.login(username='staffuser', password='staffpassword')

    def test_orders_export_view(self):
        response = self.client.get(reverse('shopapp:orders_export'))

        self.assertEqual(response.status_code, 200)

        expected_data = [
            {
                'pk': 1,
                'promocode': 'CODE1',
                'delivery_address': 'Address 1',
                'user_pk': 1,
                'products': [1]
            },
            {
                'pk': 2,
                'promocode': 'CODE2',
                'delivery_address': 'Address 2',
                'user_pk': 1,
                'products': []
            }
        ]

        self.assertJSONEqual(response.content.decode(), {'orders': expected_data})