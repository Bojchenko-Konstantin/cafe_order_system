from decimal import Decimal

from django.test import Client, TestCase
from django.urls import reverse

from ..models import MenuItem, Order


class OrderViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.menu_item = MenuItem.objects.create(
            name="Coffee",
            price=Decimal('5.00'),
        )

    def test_order_list_view(self):
        response = self.client.get(reverse('order_list'))
        self.assertEqual(response.status_code, 200)

    def test_order_create_view(self):
        response = self.client.post(
            reverse('order_create'),
            {
                'table_number': 1,
                'items[0].menu_item': self.menu_item.id,
                'items[0].quantity': 2,
            },
        )
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Order.objects.count(), 1)
