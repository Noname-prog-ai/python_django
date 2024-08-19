from django.contrib import admin

# Register your models here.
from .models import Product, Order

class OrderInline(admin.TabularInline):
    model = Order
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'discount')
    list_filter = ('price', 'discount')
    search_fields = ('name', 'price',)
    inlines = [OrderInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Цена', {
            'fields': ('price', 'discount'),
        }),
        ('Дополнительные опции', {
            'fields': ('is_archived',),
            'classes': ('collapse',),
        }),
    )

    # Групповое действие для архивации
    actions = ['archive_selected']

    def archive_selected(self, request, queryset):
        queryset.update(is_archived=True)
        self.message_user(request, "Выбранные записи успешно заархивированы.")
    archive_selected.short_description = "Архивировать выбранные записи"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'order_date')
    search_fields = ('product__name',)  # Поиск по имени продукта