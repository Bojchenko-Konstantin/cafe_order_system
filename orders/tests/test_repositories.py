from decimal import Decimal

from django.test import TestCase

from ..domain.entities import Order as OrderEntity
from ..domain.entities import OrderItem as OrderItemEntity
from ..infrastructure.models import MenuItem, Order
from ..infrastructure.repositories import OrderRepository


class OrderRepositoryTest(TestCase):
    def setUp(self):
        self.repository = OrderRepository()
        self.menu_item = MenuItem.objects.create(
            name="Coffee",
            price=Decimal('5.00'),
        )

    def test_create_order(self):
        order_entity = OrderEntity(
            table_number=1,
            items=[OrderItemEntity(menu_item=self.menu_item, quantity=2)],
            status='pending',
            total_price=Decimal('0.00'),
        )
        order = self.repository.create(order_entity)
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.total_price, Decimal('10.00'))

    def test_get_by_id(self):
        order = Order.objects.create(
            table_number=1,
            total_price=Decimal('0.00'),
        )
        found_order = self.repository.get_by_id(order.id)
        self.assertEqual(found_order.id, order.id)

    def test_update_order(self):
        order = Order.objects.create(
            table_number=1,
            total_price=Decimal('0.00'),
        )
        updated_order = self.repository.update(order.id, status="ready")
        self.assertEqual(updated_order.status, "ready")

    def test_delete_order(self):
        order = Order.objects.create(
            table_number=1,
            total_price=Decimal('0.00'),
        )
        self.repository.delete(order.id)
        self.assertFalse(Order.objects.filter(id=order.id).exists())
