from django.contrib import admin

# Register your models here.
from .models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'discount', 'archived')  # Выводим эти поля в списке
    search_fields = ('name', 'price')  # Поля для поиска

    actions = ['archive_products']  # Добавляем действие для архивации

    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price Info', {
            'fields': ('price', 'discount')
        }),
        ('Extra Options', {
            'fields': ('archived',),
            'classes': ('collapse',)  # Секция свернута
        }),
    )

    def archive_products(self, request, queryset):
        queryset.update(archived=True)
        self.message_user(request, "Выбранные продукты были заархивированы.")

    archive_products.short_description = "Заархивировать выделенные продукты"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'total_price')  # Поля для отображения
    search_fields = ('product__name', 'quantity')  # Поля для поиска