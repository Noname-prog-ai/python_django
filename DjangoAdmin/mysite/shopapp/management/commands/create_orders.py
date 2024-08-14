from django.core.management.base import BaseCommand
from shopapp.models import Order, Product
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create sample orders'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        products = Product.objects.all()

        if not products.exists() or not users.exists():
            self.stdout.write(self.style.ERROR('Ensure you have products and users before creating orders.'))
            return

        orders_data = [
            {"customer_name": "John Doe", "customer_address": "123 Main St", "user": users.first()},
            {"customer_name": "Jane Smith", "customer_address": "456 Side St", "user": users.last()},
        ]

        for data in orders_data:
            order, _ = Order.objects.get_or_create(**data)
            order.products.add(*products)  # Add all products to each order
            self.stdout.write(self.style.SUCCESS(f'Order "{data["customer_name"]}" created.'))