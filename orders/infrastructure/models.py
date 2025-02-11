from decimal import Decimal

from django.db import models


class MenuItem(models.Model):
    """A model to represent a menu item."""

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Order(models.Model):
    """A model for order representation."""

    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.IntegerField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00')
    )

    def update_total(self):
        """Updates the total cost of the order based
        on the cost of all menu items in the order.
        """
        self.total_price = sum(item.subtotal() for item in self.items.all())
        self.save()


class OrderItem(models.Model):
    """A model to represent the point of order."""

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
    )
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        """Calculates the total cost of this order item."""
        return self.menu_item.price * Decimal(self.quantity)
