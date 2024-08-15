from django.core.management.base import BaseCommand
from shopapp.models import Product


class Command(BaseCommand):
    help = 'Create sample products'

    def handle(self, *args, **kwargs):
        productsdata =
        {"name": "Product 1", "description": "Description 1", "price": 10.0, "quantity": 100},
        {"name": "Product 2", "description": "Description 2", "price": 20.0, "quantity": 200},
        {"name": "Product 3", "description": "Description 3", "price": 30.0, "quantity": 300},

    for data in productsdata:
        Product.objects.getorcreate(**data)
        self.stdout.write(self.style.SUCCESS(f'Product "{data["name"]}" created/exists.'))