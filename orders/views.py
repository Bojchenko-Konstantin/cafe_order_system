from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MenuItem, Order
from .repositories import OrderRepository
from .serializers import OrderSerializer
from .services import process_order_creation
from .use_cases import (
    CalculateRevenueUseCase,
    DeleteOrderUseCase,
    UpdateOrderStatusUseCase,
)

order_repository = OrderRepository()


def order_list(request: HttpRequest) -> HttpResponse:
    """
    Show a list of orders with the ability to filter by status.

    """
    status_filter = request.GET.get('status')
    orders = OrderRepository.get_all()

    if status_filter:
        orders = orders.filter(status=status_filter)

    menu_items = MenuItem.objects.all()
    return render(
        request,
        'orders/order_list.html',
        {
            'orders': orders,
            'menu_items': menu_items,
            'status_filter': status_filter,
        },
    )


def order_create(request: HttpRequest) -> HttpResponse:
    """
    Handles the creation of a new order.

    If the request method is POST, a new order is created
    and redirects to the list of orders.
    If the method is GET, the form for creating an order is displayed.

    """
    if request.method == 'POST':
        process_order_creation(request)
        return redirect('order_list')

    menu_items = MenuItem.objects.all()
    return render(
        request,
        'orders/order_form.html',
        {'menu_items': menu_items},
    )


def order_update(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Handles updating the status of an existing order.

    If the request method is POST, the order status is updated
    and redirects to the order list.
    If the method is GET, the form for order editing is displayed.

    """
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        use_case = UpdateOrderStatusUseCase(order_repository)
        use_case.execute(order_id, status)
        return redirect('order_list')
    return render(request, 'orders/order_form.html', {'order': order})


@require_POST
def order_update_status(request, order_id):
    """
    Updates the status of an order by order ID.

    """
    status = request.POST.get('status')
    use_case = UpdateOrderStatusUseCase(order_repository)
    use_case.execute(order_id, status)
    return redirect('order_list')


def order_delete(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Delete order by its order ID.

    """
    use_case = DeleteOrderUseCase(order_repository)
    use_case.execute(order_id)
    return redirect('order_list')


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    """
    Show the details of a specific order.

    """
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})


def revenue(request: HttpRequest) -> HttpResponse:
    """
    Calculates and displays total revenue from all orders.

    """
    use_case = CalculateRevenueUseCase(order_repository)
    total_revenue = use_case.execute()
    return render(
        request,
        'orders/revenue.html',
        {'total_revenue': total_revenue},
    )


@api_view(['GET', 'POST'])
def order_api_list(request):
    if request.method == 'GET':
        orders = OrderRepository.get_all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def order_api_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        order.delete()
        return Response(status=204)
