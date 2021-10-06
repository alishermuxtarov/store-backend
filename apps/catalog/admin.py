from django.contrib import admin
from django.db.models import Count, Sum

from . import models
from .models import Order


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ['category', 'name', 'price', 'image', 'description']
    list_display = ['id', 'name', 'price', 'category']
    list_display_links = ['name']
    search_fields = ['name', 'description']
    list_filter = ['category']
    ordering = ['category', 'name']


class OrderInline(admin.TabularInline):
    model = models.OrderItem
    fields = ['product', 'quantity', 'price', 'amount']
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ['user', 'email', 'address']
    list_display = ['id', 'user', 'address', 'items_count', 'total_amount']
    list_display_links = ['user']
    search_fields = ['address', 'email']
    ordering = ['-id']
    inlines = [OrderInline]

    def get_queryset(self, request):
        return Order.objects.annotate(items_count=Count('items'), total_amount=Sum('items__price'))

    @staticmethod
    def items_count(obj):
        return obj.items_count

    @staticmethod
    def total_amount(obj):
        return '$%d' % (obj.total_amount or 0)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
