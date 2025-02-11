from decimal import Decimal
from django.core.exceptions import ValidationError
from ..infrastructure.models import MenuItem, OrderItem


def create_order_item(order, item):
    """Create OrderItem for one order."""
    try:
        menu_item = MenuItem.objects.get(name=item.menu_item.name)
        OrderItem.objects.create(
            order=order,
            menu_item=menu_item,
            quantity=item.quantity,
        )
        return Decimal(str(menu_item.price)) * Decimal(str(item.quantity))
    except MenuItem.DoesNotExist:
        raise ValidationError(f"Menu item {item.menu_item.name} does not exist.")
    except Exception as e:
        raise Exception(f"Error creating order item: {e}")
