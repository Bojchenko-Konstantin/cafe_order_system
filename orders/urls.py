from django.urls import path

from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/update/', views.order_update, name='order_update'),
    path(
        '<int:order_id>/update-status/',
        views.order_update_status,
        name='order_update_status',
    ),
    path('<int:order_id>/delete/', views.order_delete, name='order_delete'),
    path('revenue/', views.revenue, name='revenue'),
    path('api/orders/', views.order_api_list, name='order_api_list'),
    path(
        'api/orders/<int:order_id>/',
        views.order_api_detail,
        name='order_api_detail',
    ),
]
