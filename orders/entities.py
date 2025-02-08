from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List


@dataclass
class MenuItem:
    """Represents a menu item."""

    name: str
    price: Decimal


@dataclass
class OrderItem:
    """
    Represents an order item,
    consisting of a menu item and its quantity.

    """

    menu_item: MenuItem
    quantity: int


@dataclass
class Order:
    """
    Represents an order containing information
    about the table, ordered items, and order status.

    """

    table_number: int
    items: List[OrderItem]
    status: str
    total_price: Decimal = Decimal('0.00')
    id: int | None = None
    created_at: datetime | None = None

    def calculate_total(self):
        """
        Calculates the total price of the order and updates
        the total_price attribute.

        """
        self.total_price = sum(
            item.menu_item.price * item.quantity for item in self.items
        )
