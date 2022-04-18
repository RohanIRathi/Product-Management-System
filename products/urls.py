from django.urls import re_path

from . import views

urlpatterns = [
	re_path(r'getAllProducts\/?$', views.get_products_list, name='getAllProducts'),
	re_path(r'fetchProductDetails/<int:product_id>\/?$', views.get_product_details, name='fetchProductDetails'),
	re_path(r'addProduct\/?$', views.add_product, name='addProduct'),
	re_path(r'updateProduct/<int:product_id>\/?$', views.update_product, name='updateProduct'),
]