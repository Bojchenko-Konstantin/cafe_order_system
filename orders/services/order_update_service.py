from django.core.exceptions import ValidationError
from ..infrastructure.models import Order
from .exceptions import OrderNotFoundError, OrderServiceError


def update_order_attributes(order_id: int, **kwargs) -> Order:
    """Обновляет атрибуты заказа по его ID."""
    try:
        order = Order.objects.get(id=order_id)
        for key, value in kwargs.items():
            setattr(order, key, value)
        order.save()
        return order
    except Order.DoesNotExist:
        raise OrderNotFoundError(f"Order with ID {order_id} does not exist.")
    except ValidationError as e:
        raise OrderServiceError(f"Validation error while updating order {order_id}: {e}")
    except Exception as e:
        raise OrderServiceError(f"Error updating order {order_id}: {e}")
