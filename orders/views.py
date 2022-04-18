from datetime import datetime
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
			retailer_id = int(request.GET['retailer'])
		except:
			retailer_id = None
		try:
			distributor = User.objects.get(pk=user_id)
			if distributor.is_superuser and distributor.is_staff:
				orders = Order.objects.filter(DistributorId=distributor).order_by('-CreationDate')
				if retailer_id:
					retailer = User.objects.get(pk=retailer_id)
					orders = orders.filter(RetailerId=retailer)
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
		return JsonResponse({'orders': retailer_orders, 'success': True}, status=200)

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
		data = json.loads(request.body)
		distributor = User.objects.get(pk=data['distributor'])
		retailer = User.objects.get(pk=data['retailer'])
		totalQuantity = data['totalQuantity']
		totalAmount = data['totalAmount']
		products = data['products']
		product_list, products_to_update = [], []
		order = Order(
			DistributorId=distributor,
			RetailerId=retailer,
			TotalQuantity=totalQuantity,
			TotalAmount=totalAmount
		)
		try:
			order.save()
			totalAmount, totalQuantity = 0, 0
			for orderproduct in products:
				print(orderproduct)
				product = Product.objects.get(pk=orderproduct['product'])
				if product.Quantity < orderproduct['quantity']:
					raise Exception('Insufficient Quantity')
				order_product = OrderProduct(
						Order=order,
						Product=product,
						Discount=orderproduct['discount'],
						Quantity=orderproduct['quantity']
						)
				totalAmount = float(totalAmount) + float((float(product.Price) - (float(product.Price) * float(order_product.Discount) * 0.01)) * float(order_product.Quantity))
				totalQuantity = float(totalQuantity) + float(order_product.Quantity)
				product.Quantity -= order_product.Quantity
				products_to_update.append(product)
				product_list.append(order_product)
			order.TotalAmount = totalAmount
			order.TotalQuantity = totalQuantity
			if float(retailer.PendingAmount) + float(order.TotalAmount) > float(retailer.CreditLimit):
				raise Exception('Insufficient Credit Limit')
			retailer.PendingAmount = float(retailer.PendingAmount) + float(order.TotalAmount)
			OrderProduct.objects.bulk_create(product_list)
			order.save()
			retailer.save()
			for product in products_to_update:
				product.save()
			return JsonResponse({'success': True, 'created order': order.json()}, status=200)
		except Exception as e:
			print(e)
			order.delete()
			return JsonResponse({'success': False, 'error': str(e) or 'Something Went Wrong'}, status=500)

def order_paid(request):
	order_id = int(request.GET['order'])
	session = request.session.decode(request.headers['Session'])
	user_id = session['id']
	try:
		distributor = User.objects.get(pk=user_id)
		if not distributor.is_superuser or not distributor.is_staff:
			raise User.DoesNotExist()
		order = Order.objects.get(pk=order_id)
		print(order.DistributorId == distributor)
		if order.DistributorId != distributor:
			raise Order.DoesNotExist()
		order.PaymentDate = datetime.now()
		order.save()
		return JsonResponse({'success': True, 'message': 'Order marked as paid'}, status=200)
	except User.DoesNotExist:
		return JsonResponse({'success': False, 'error': 'Action Unauthoriezd'}, status=403)
	except Order.DoesNotExist:
		return JsonResponse({'success': False, 'error': 'Invalid Order Selected'}, status=404)