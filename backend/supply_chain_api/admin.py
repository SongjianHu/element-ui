from django.contrib import admin
from .models import Supplier, Category, Product, PurchaseOrder, PurchaseOrderItem, Inventory


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email', 'created_at']
    search_fields = ['name', 'contact_person', 'phone', 'email']
    list_filter = ['created_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'supplier', 'unit_price', 'stock_quantity', 'min_stock_level']
    search_fields = ['name', 'sku', 'description']
    list_filter = ['category', 'supplier', 'created_at']
    autocomplete_fields = ['category', 'supplier']


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    autocomplete_fields = ['product']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'supplier', 'order_date', 'expected_delivery_date', 'status', 'total_amount', 'created_by']
    list_filter = ['status', 'order_date', 'supplier']
    search_fields = ['order_number', 'supplier__name']
    autocomplete_fields = ['supplier']
    inlines = [PurchaseOrderItemInline]
    readonly_fields = ['total_amount', 'created_by']


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'current_stock', 'reserved_stock', 'available_stock', 'last_updated']
    search_fields = ['product__name', 'product__sku']
    list_filter = ['last_updated']
    readonly_fields = ['available_stock', 'last_updated'] 