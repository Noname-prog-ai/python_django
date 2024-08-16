from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связь с Product
    quantity = models.IntegerField()  # Количество
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Общая цена

    def __str__(self):
        return f"Order by {self.customer_name} at {self.created_at}"