from django.urls import path

from . import views

urlpatterns = [
	path('getAllProducts/', views.get_products_list, name='getAllProducts'),
	path('fetchProductDetails/<int:product_id>/', views.get_product_details, name='fetchProductDetails'),
	path('addProduct/', views.add_product, name='addProduct'),
	path('updateProduct/<int:product_id>/', views.update_product, name='updateProduct'),
]