from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Order, Product
from django.contrib.auth.models import Permission

User = get_user_model()

class OrderDetailViewTest(TestCase):

    def setUp(self):
        # Создание пользователя и вход
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.is_staff = True
        permission = Permission.objects.get(codename='view_order')
        self.user.user_permissions.add(permission)
        self.user.save()

        # Вход пользователя в систему
        self.client.login(username='testuser', password='testpassword')

        # Создание заказа после входа
        self.order = Order.objects.create(
            user=self.user,
            address='Test Address'
        )

    def tearDown(self):
        # Удаление заказа
        self.order.delete()
        # Удаление пользователя
        self.user.delete()

    def test_order_detail_view(self):
        response = self.client.get(
            reverse('shopapp:order_details', args=[self.order.pk])  # Исправлено имя URL на order_details
        )

        # Проверка статуса ответа
        self.assertEqual(response.status_code, 200)
        # Проверка содержимого ответа
        self.assertContains(response, self.order.address)
        # Проверка существующих атрибутов
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание фикстур пользователей и продуктов
        cls.user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
        permission = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission)
        cls.user.save()

        cls.product1 = Product.objects.create(name='Product 1')
        cls.product2 = Product.objects.create(name='Product 2')

        cls.order1 = Order.objects.create(user=cls.user, address='Address 1')
        cls.order1.products.add(cls.product1)  # Связываем заказ с продуктом
        cls.order2 = Order.objects.create(user=cls.user, address='Address 2')
        cls.order2.products.add(cls.product2)  # Связываем заказ с продуктом

    def setUp(self):
        # Вход пользователя с правами
        self.client.login(username='staffuser', password='staffpassword')

    def tearDown(self):
        # Удаление заказов после тестов
        self.order1.delete()
        self.order2.delete()
        # Удаление пользователя
        self.user.delete()
        self.product1.delete()
        self.product2.delete()

    def test_orders_export_view(self):
        response = self.client.get(
            reverse('shopapp:orders_export')  # Убедитесь, что этот URL также существует в urls.py
        )

        # Проверка статуса ответа
        self.assertEqual(response.status_code, 200)
        # Получение всех заказов с использованием select_related и prefetch_related
        orders = Order.objects.select_related('user').prefetch_related('products').all()

        # Проверка структуры ответа
        expected_data = [
            {
                'id': order.pk,
                'address': order.address,
                'user_id': order.user.pk,
                'product_ids': [product.pk for product in order.products.all()]
            }
            for order in orders
        ]

        self.assertJSONEqual(response.content, expected_data)