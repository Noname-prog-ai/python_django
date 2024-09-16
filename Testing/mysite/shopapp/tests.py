from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Order  # Импортируйте вашу модель заказа

User = get_user_model()


class OrderDetailViewTest(TestCase):

    def setUp(self):
        # Создание пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.is_staff = True
        self.user.save()

        # Создание заказа
        self.order = Order.objects.create(
            user=self.user,
            address='Test Address',
            promo_code='TEST123'
        )

        # Учет в контексте
        self.client.login(username='testuser', password='testpassword')

    def tearDown(self):
        # Удаление заказа
        self.order.delete()
        # Удаление пользователя
        self.user.delete()

    def test_order_detail_view(self):
        response = self.client.get(
            reverse('order_detail', args=[self.order.pk]))  # Убедитесь, что используете правильный URL

        # Проверка статуса ответа
        self.assertEqual(response.status_code, 200)
        # Проверка содержимого ответа
        self.assertContains(response, self.order.address)
        self.assertContains(response, self.order.promo_code)
        self.assertEqual(response.context['order'].pk, self.order.pk)


class OrdersExportViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание нескольких заказов в фикстурах
        cls.user = User.objects.create_user(username='staffuser', password='staffpassword', is_staff=True)
        cls.order1 = Order.objects.create(user=cls.user, address='Address 1', promo_code='CODE1')
        cls.order2 = Order.objects.create(user=cls.user, address='Address 2', promo_code='CODE2')

    def setUp(self):
        # Вход пользователя с правами
        self.client.login(username='staffuser', password='staffpassword')

    def tearDown(self):
        # Удаление заказов после тестов
        self.order1.delete()
        self.order2.delete()
        # Удаление пользователя
        self.user.delete()

    def test_orders_export_view(self):
        response = self.client.get(reverse('orders_export'))  # Убедитесь, что используете правильный URL

        # Проверка статуса ответа
        self.assertEqual(response.status_code, 200)
        # Проверка структуры ответа
        expected_data = [
            {'id': self.order1.pk, 'address': self.order1.address, 'promo_code': self.order1.promo_code,
             'user_id': self.user.pk, 'product_ids': [product.pk for product in self.order1.products.all()]},
            {'id': self.order2.pk, 'address': self.order2.address, 'promo_code': self.order2.promo_code,
             'user_id': self.user.pk, 'product_ids': [product.pk for product in self.order2.products.all()]}
        ]

        self.assertJSONEqual(response.content, expected_data)