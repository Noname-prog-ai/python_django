from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Order, Product  # Импортируйте ваши модели


class OrdersExportViewTests(TestCase):

    def setUp(self):
        # Создаем тестового пользователя, который не является staff
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Создаем тестового пользователя, который является staff
        self.staff_user = User.objects.create_user(username='staffuser', password='staffpass', is_staff=True)

        # Создаем тестовые продукты и заказы
        self.product1 = Product.objects.create(name='Product 1', price=10.00)
        self.product2 = Product.objects.create(name='Product 2', price=15.00)

        self.order1 = Order.objects.create(
            delivery_address='123 Test St',
            promocode='PROMO10',
            user=self.staff_user
        )
        self.order1.products.add(self.product1, self.product2)

        self.order2 = Order.objects.create(
            delivery_address='456 Sample Ave',
            promocode='PROMO20',
            user=self.staff_user
        )
        self.order2.products.add(self.product1)

    def test_orders_export_view_access_denied_for_non_staff(self):
        # Пытаемся получить доступ к представлению без прав доступа и проверяем статус 403 Forbidden
        response = self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 403)

    def test_orders_export_view_access_granted_for_staff(self):
        # Пытаемся получить доступ к представлению с правами доступа и проверяем статус 200 OK
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.get(reverse('shopapp:orders_export'))
        self.assertEqual(response.status_code, 200)

    def test_orders_export_view_json_structure(self):
        # Проверяем структуру JSON-ответа
        self.client.login(username='staffuser', password='staffpass')
        response = self.client.get(reverse('shopapp:orders_export'))

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertIn('orders', data)
        self.assertIsInstance(data['orders'], list)
        self.assertEqual(len(data['orders']), 2)

        # Проверяем данные по каждому заказу
        order1_data = data['orders'][0]
        self.assertIn('pk', order1_data)
        self.assertIn('delivery_address', order1_data)
        self.assertIn('promocode', order1_data)
        self.assertIn('user_pk', order1_data)
        self.assertIn('products', order1_data)

        self.assertEqual(order1_data['pk'], self.order1.pk)
        self.assertEqual(order1_data['delivery_address'], self.order1.delivery_address)
        self.assertEqual(order1_data['promocode'], self.order1.promocode)
        self.assertEqual(order1_data['user_pk'], self.order1.user.pk)
        self.assertEqual(set(order1_data['products']), {self.product1.pk, self.product2.pk})
