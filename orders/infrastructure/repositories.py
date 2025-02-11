from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import QuerySet

from orders.services.exceptions import MenuItemNotFoundError, OrderNotFoundError, OrderServiceError

from ..domain.entities import Order as OrderEntity
from ..infrastructure.models import MenuItem, Order, OrderItem
from ..domain.repositories import BaseOrderRepository

from ..services.order_item_service import create_order_item 

class OrderRepository(BaseOrderRepository):
    def get_all(self) -> QuerySet[Order]:
        """Get a list of all orders from the database"""
        try:
            return Order.objects.prefetch_related('items').all()
        except Exception as e:
            raise OrderServiceError(f"Error fetching all orders: {e}")

    def get_by_id(self, order_id: int) -> Order | None:
        """Get order by ID."""
        try:
            return Order.objects.prefetch_related('items').get(id=order_id)
        except Order.DoesNotExist:
            raise OrderNotFoundError(f"Order with ID {order_id} does not exist.")
        except Exception as e:
            raise OrderServiceError(f"Error fetching order by ID {order_id}: {e}")

    def create(self, order_entity: OrderEntity) -> Order:
        """Creates a new order based on the order entity."""
        try:
            order = Order.objects.create(
                table_number=order_entity.table_number,
                status=order_entity.status,
                total_price=Decimal('0.00'),
            )

            total_price = Decimal('0.00')
            for item in order_entity.items:
                try:
                    total_price += create_order_item(order, item)
                except ValidationError as e:
                    raise MenuItemNotFoundError(str(e))
                except Exception as e:
                    raise OrderServiceError(f"Error creating order item: {e}")

            order.total_price = total_price
            order.save()

            return order
        except Exception as e:
            raise OrderServiceError(f"Error creating order: {e}")

    def update(self, order_id: int, **kwargs) -> Order | None:
        """Updates an existing order by its order ID."""
        try:
            order = Order.objects.get(id=order_id)
            for key, value in kwargs.items():
                setattr(order, key, value)
            order.save()
            return order
        except Order.DoesNotExist:
            raise OrderNotFoundError(f"Order with ID {order_id} does not exist.")
        except Exception as e:
            raise OrderServiceError(f"Error updating order {order_id}: {e}")

    def delete(self, order_id: int) -> None:
        """Deletes an order by its order ID."""
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
        except Order.DoesNotExist:
            raise OrderNotFoundError(f"Order with ID {order_id} does not exist.")
        except Exception as e:
            raise OrderServiceError(f"Error deleting order {order_id}: {e}")
