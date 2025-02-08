from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .services import process_order_creation 

from .models import MenuItem, Order
from .repositories import OrderRepository
from .use_cases import (
    CalculateRevenueUseCase,
    DeleteOrderUseCase,
    UpdateOrderStatusUseCase,
)

order_repository = OrderRepository()


def order_list(request: HttpRequest) -> HttpResponse:
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
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        use_case = UpdateOrderStatusUseCase(order_repository)
        use_case.execute(order_id, status)
        return redirect('order_list')
    return render(request, 'orders/order_form.html', {'order': order})


@require_POST
def order_update_status(request, order_id):
    status = request.POST.get('status')
    use_case = UpdateOrderStatusUseCase(order_repository)
    use_case.execute(order_id, status)
    return redirect('order_list')


def order_delete(request: HttpRequest, order_id: int) -> HttpResponse:
    use_case = DeleteOrderUseCase(order_repository)
    use_case.execute(order_id)
    return redirect('order_list')


def order_detail(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_detail.html', {'order': order})


def revenue(request: HttpRequest) -> HttpResponse:
    use_case = CalculateRevenueUseCase(order_repository)
    total_revenue = use_case.execute()
    return render(request, 'orders/revenue.html', {'total_revenue': total_revenue})
