from decimal import Decimal

from django.test import TestCase

from ..domain.entities import OrderItem as OrderItemEntity
from ..infrastructure.models import MenuItem, Order
from ..infrastructure.repositories import OrderRepository
from ..use_cases import (
    CreateOrderUseCase,
    DeleteOrderUseCase,
    UpdateOrderStatusUseCase,
)


class CreateOrderUseCaseTest(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name="Coffee",
            price=Decimal('5.00'),
        )
        self.repository = OrderRepository()

    def test_create_order(self):
        use_case = CreateOrderUseCase(self.repository)
        items_data = [
            OrderItemEntity(menu_item=self.menu_item, quantity=2),
        ]
        order = use_case.execute(1, items_data)
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.total_price, Decimal('10.00'))


class UpdateOrderStatusUseCaseTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            table_number=1,
            total_price=Decimal('0.00'),
        )
        self.repository = OrderRepository()

    def test_update_order_status(self):
        use_case = UpdateOrderStatusUseCase(self.repository)
        updated_order = use_case.execute(self.order.id, "ready")
        self.assertEqual(updated_order.status, "ready")


class DeleteOrderUseCaseTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            table_number=1,
            total_price=Decimal('0.00'),
        )
        self.repository = OrderRepository()

    def test_delete_order(self):
        use_case = DeleteOrderUseCase(self.repository)
        use_case.execute(self.order.id)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())
