from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.name