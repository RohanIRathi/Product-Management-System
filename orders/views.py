import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from home.models import User
from products.models import Product
from .models import Order, OrderProduct

# Create your views here.

def get_distributor_orders(request):
	if request.method == 'GET':
		user_id = request.session.decode(request.headers['Session'])['id']
		try:
			distributor = User.objects.get(pk=user_id)
			if distributor.is_superuser and distributor.is_staff:
				orders = Order.objects.filter(DistributorId=distributor).order_by('-CreationDate')
				distributor_orders = [order.json() for order in orders]
				return JsonResponse({'success': True, 'orders': distributor_orders}, status=200)
			else:
				return JsonResponse({'success': False, 'error': 'Access Denied'}, status=403)
		except:
			return JsonResponse({'success': False, 'error': 'User Does Not Exist'}, status=400)

def get_retailer_orders(request):
	if request.method == 'GET':
		retailer_id = request.session.decode(request.headers['Session'])['id']
		try:
			distributor_id = request.GET['distributor']
		except:
			distributor_id = None
		orders = Order.objects.filter(RetailerId=retailer_id).order_by('-CreationDate')
		if distributor_id:
			orders = orders.filter(DistributorId=distributor_id)
		retailer_orders = [order.json() for order in orders]
        # order_products = OrderProduct.objects.filter(Order=orders)
        # print(list(order_products))
		return JsonResponse({'order': retailer_orders, 'success': True}, status=200)

def get_order_details(request, **kwargs):
	if request.method == 'GET':
		order_id = kwargs['order_id']
		try:
			order = Order.objects.get(pk=order_id)
			return JsonResponse({'order': order.json(), 'success': True}, status=200)
		except Order.DoesNotExist:
			return JsonResponse({'success': False, 'error': 'Invalid Order Id'}, status=400)
		except:
			return JsonResponse({'success': False, 'error': 'Something Went Wrong'}, status=500)

@csrf_exempt
def add_order(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			distributor = User.objects.get(pk=data['distributor'])
			retailer = User.objects.get(pk=data['retailer'])
			totalQuantity = data['totalQuantity']
			totalAmount = data['totalAmount']
			products = data['products']
			product_list = []
			order = Order(
				DistributorId=distributor,
				RetailerId=retailer,
				TotalQuantity=totalQuantity,
				TotalAmount=totalAmount
			)
			order.save()
			totalAmount, totalQuantity = 0, 0
			for orderproduct in products:
					product = Product.objects.get(pk=orderproduct['id'])
					if product.Quantity < orderproduct['quantity']:
						raise Exception('Insufficient Quantity')
					order_product = OrderProduct(
							Order=order,
							Product=product,
							Discount=orderproduct['discount'],
							Quantity=orderproduct['quantity']
							)
					totalAmount += (float(product.Price) - (float(product.Price) * float(order_product.Discount) * 0.01)) * order_product.Quantity
					totalQuantity += order_product.Quantity
					product_list.append(order_product)
			order.TotalAmount = totalAmount
			order.TotalQuantity = totalQuantity
			if retailer.PendingAmount + order.TotalAmount > retailer.CreditLimit:
				raise Exception('Insufficient Credit Limit')
			retailer.PendingAmount += order.TotalAmount
			OrderProduct.objects.bulk_create(product_list)
			order.save()
			retailer.save()
			return JsonResponse({'created order': order.json()}, status=200)
		except Exception as e:
			print(e)
			order.delete()
			return JsonResponse({'success': False, 'error': 'Something Went Wrong'}, status=500)