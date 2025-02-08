from django.contrib import admin

from .models import Order, OrderItem, MenuItem


class OrderItemInline(admin.TabularInline):
    """Inline-class for displaying order items in the admin panel."""
    model = OrderItem
    extra = 1
    fields = ['menu_item', 'quantity']
    readonly_fields = ['subtotal']

    def subtotal(self, instance):
        """Calculates and returns the total cost of this order item."""
        return instance.subtotal()

    subtotal.short_description = 'Subtotal'

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin class for managing menu items."""
    list_display = ['name', 'price']
    search_fields = ['name']
    list_filter = ['price']
    ordering = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin class for order management."""
    list_display = [
        'id',
        'table_number',
        'total_price',
        'status',
        'created_at',
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['table_number']
    inlines = [OrderItemInline]
    readonly_fields = ['total_price', 'created_at']
    list_editable = ['status']

    fieldsets = [
        (None, {'fields': ['table_number', 'status']}),
        ('Details', {'fields': ['total_price', 'created_at']}),
    ]

    def save_model(self, request, obj, form, change):
        """Saves a copy of the order and updates the order total."""
        super().save_model(request, obj, form, change)
        obj.update_total()


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin class for managing order points."""
    list_display = ['order', 'menu_item', 'quantity', 'subtotal']
    list_filter = ['order__status']
    search_fields = ['order__id', 'menu_item__name']

    def subtotal(self, obj):
        """Calculates and returns the total cost of this order item."""
        return obj.subtotal()

    subtotal.short_description = 'Subtotal'
