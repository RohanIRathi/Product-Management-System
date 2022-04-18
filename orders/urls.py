from django.urls import path

from . import views

urlpatterns = [
    path('getDistributorOrders/', views.get_distributor_orders, name='getDistributorOrders'),
	path('getRetailerOrders/', views.get_retailer_orders, name='getRetailerOrders'),
	path('fetchOrderDetails/<int:order_id>/', views.get_order_details, name='fetchOrderDetails'),
	path('addOrder/', views.add_order, name='addOrder'),
	path('orderPaid', views.order_paid, name="orderPaid"),
]