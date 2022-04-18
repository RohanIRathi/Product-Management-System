from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'getDistributorOrders/?$', views.get_distributor_orders, name='getDistributorOrders'),
	re_path(r'getRetailerOrders/?$', views.get_retailer_orders, name='getRetailerOrders'),
	path('fetchOrderDetails/<int:order_id>/', views.get_order_details, name='fetchOrderDetails'),
	re_path(r'addOrder/?$', views.add_order, name='addOrder'),
	re_path(r'orderPaid/?$', views.order_paid, name="orderPaid"),
]