from decimal import Decimal

from django.test import TestCase

from ..infrastructure.models import MenuItem, Order, OrderItem


class MenuItemModelTest(TestCase):
    def test_create_menu_item(self):
        item = MenuItem.objects.create(
            name="Coffee",
            price=Decimal('5.00'),
        )
        self.assertEqual(item.name, "Coffee")
        self.assertEqual(item.price, Decimal('5.00'))


class OrderModelTest(TestCase):
    def test_create_order(self):
        order = Order.objects.create(
            table_number=1,
            total_price=Decimal('0.00'),
        )
        self.assertEqual(order.table_number, 1)
        self.assertEqual(order.status, "pending")


class OrderItemModelTest(TestCase):
    def test_create_order_item(self):
        menu_item = MenuItem.objects.create(
            name="Tea",
            price=Decimal('3.00'),
        )
        order = Order.objects.create(
            table_number=2,
            total_price=Decimal('0.00'),
        )
        order_item = OrderItem.objects.create(
            order=order, menu_item=menu_item, quantity=2
        )
        self.assertEqual(order_item.subtotal(), Decimal('6.00'))
