from decimal import Decimal
from typing import List

from .entities import OrderItem as OrderItemEntity
from .models import Order as OrderModel
from .models import OrderItem as OrderItemModel
from .repositories import OrderRepository


class CreateOrderUseCase:
    def __init__(self, repository):
        self.repository = repository

    def execute(
        self, table_number: int, items_data: List[OrderItemEntity]
    ) -> OrderModel:
        """
        Creates a new order with the specified
        table number and order items.

        """
        order = OrderModel.objects.create(
            table_number=table_number,
            status='pending',
            total_price=Decimal('0.00'),
        )

        total_price = Decimal('0.00')
        for item_data in items_data:
            menu_item = item_data.menu_item
            quantity = item_data.quantity
            subtotal = Decimal(str(menu_item.price)) * Decimal(str(quantity))

            OrderItemModel.objects.create(
                order=order, menu_item=menu_item, quantity=quantity
            )

            total_price += subtotal

        order.total_price = total_price
        order.save()

        return order


class UpdateOrderStatusUseCase:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self, order_id: int, status: str) -> OrderModel | None:
        """
        Updates the status of an existing order by order ID.

        """
        return self.repository.update(order_id, status=status)


class DeleteOrderUseCase:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self, order_id: int) -> None:
        """
        Delete order by order ID.

        """
        self.repository.delete(order_id)


class CalculateRevenueUseCase:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def execute(self) -> Decimal:
        """
        Calculates the total revenue from all paid orders.

        """
        orders = self.repository.get_all().filter(status='paid')
        return sum(order.total_price for order in orders)
