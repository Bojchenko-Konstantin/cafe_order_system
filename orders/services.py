from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from .entities import OrderItem as OrderItemEntity
from .models import MenuItem
from .repositories import OrderRepository
from .use_cases import CreateOrderUseCase

order_repository = OrderRepository()


def process_order_creation(request: HttpRequest) -> None:
    """
    Processes the data from the form and creates the order.

    """
    if request.method != 'POST':
        return

    try:
        table_number = int(request.POST.get('table_number'))
        items_data = []

        for key, value in request.POST.items():
            if key.startswith('items[') and key.endswith('].menu_item'):
                index = key.split('[')[1].split(']')[0]
                menu_item_id = int(value)
                quantity = int(request.POST.get(f'items[{index}].quantity', 1))

                menu_item = MenuItem.objects.get(id=menu_item_id)
                items_data.append(
                    OrderItemEntity(menu_item=menu_item, quantity=quantity)
                )

        use_case = CreateOrderUseCase(order_repository)
        use_case.execute(table_number, items_data)

    except (ValueError, ObjectDoesNotExist) as e:
        print(f"Error creating order: {e}")
