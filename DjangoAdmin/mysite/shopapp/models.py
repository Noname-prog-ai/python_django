from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)  # Название продукта
    description = models.TextField()  # Описание продукта
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена продукта
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Скидка
    archived = models.BooleanField(default=False)  # Поле для архивации

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связь с Product
    quantity = models.IntegerField()  # Количество
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Общая цена

    def __str__(self):
        return f"Order by {self.customer_name} at {self.created_at}"