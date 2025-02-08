from decimal import Decimal
from typing import List

from .entities import Order as OrderEntity
from .models import MenuItem, Order, OrderItem

class OrderRepository:
    @staticmethod
    def get_all() -> List[Order]:
        """Get a list of all orders from the database"""
        return Order.objects.prefetch_related('items').all()

    @staticmethod
    def get_by_id(order_id: int) -> Order | None:
        """Get order by ID."""
        try:
            return Order.objects.prefetch_related('items').get(id=order_id)
        except Order.DoesNotExist:
            return None

    @staticmethod
    def create(order_entity: OrderEntity) -> Order:
        """Creates a new order based on the order entity."""
        order = Order.objects.create(
            table_number=order_entity.table_number,
            status=order_entity.status,
            total_price=Decimal('0.00'),   
        )

        total_price = Decimal('0.00')
        for item in order_entity.items:
            OrderItem.objects.create(
                order=order,
                menu_item=MenuItem.objects.get(name=item.menu_item.name),
                quantity=item.quantity,
            )
            total_price += Decimal(str(item.menu_item.price)) * Decimal(
                str(item.quantity)
            )

        order.total_price = total_price
        order.save()

        return order

    @staticmethod
    def update(order_id: int, **kwargs) -> Order | None:
        """Updates an existing order by its order ID."""
        order = Order.objects.get(id=order_id)
        for key, value in kwargs.items():
            setattr(order, key, value)
        order.save()
        return order

    @staticmethod
    def delete(order_id: int) -> None:
        """Deletes an order by its order ID."""
        order = Order.objects.get(id=order_id)
        order.delete()
