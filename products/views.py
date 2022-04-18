import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from products.models import Product
from home.models import User

# Create your views here.

def get_products_list(request):
	if request.method == 'GET':
		products_list = Product.objects.all()
		all_products = [product.json() for product in products_list]

		return JsonResponse({'products_list': all_products, 'success': True}, status=200)
	return JsonResponse({'success': False, 'error': 'Method Not Allowed'}, status=405)

def get_product_details(request, **kwargs):
	if request.method == 'GET':
		product_id = kwargs['product_id']
		try:
			product = Product.objects.get(pk=product_id)
			return JsonResponse({'product': product.json(), 'success': True}, status=200)
		except Product.DoesNotExist:
			return JsonResponse({'success': False, 'error': 'Product does not exist'}, status=400)
		except:
			return JsonResponse({'success': False, 'error': 'Something Went Wrong'}, status=500)
	return JsonResponse({'success': False, 'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def add_product(request):
	if request.method == 'POST':
		session_data = request.headers['Session']
		user_id = request.session.decode(session_data)['id']
		try:
			User.objects.filter(is_superuser=True).filter(is_staff=True).get(pk=user_id)
			data = json.loads(request.body)
			company = data['company']
			series = data['series']
			model = data['model']
			price = data['price']
			quantity = data['quantity']

			if Product.objects.filter(Company=company).filter(Series=series).filter(Model=model).count() > 0:
				return JsonResponse({'success': False, 'error': 'Product already exists'}, status=400)

			product = Product(Company=company, Series=series, Model=model, Price=price, Quantity=quantity)
			product.save()

			return JsonResponse({'success': True, 'addedProduct': product.json()}, status=200)
		except Exception as e:
			return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
	return JsonResponse({'success': False, 'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def update_product(request, **kwargs):
	if request.method == 'PUT':
		product_id = kwargs['product']
		try:
			product = Product.objects.get(pk=product_id)
			data = json.loads(request.body)
			price = data.get('price', product.Price)
			quantity = data.get('quantity', product.Quantity)
			product.Price = price
			product.Quantity = quantity
			product.save()
			return JsonResponse({'success': True, 'updated product': product.json()}, status=200)
		except Product.DoesNotExist:
			return JsonResponse({'success': False, 'error': 'Product Does Not Exist'}, status=400)
		except:
			return JsonResponse({'success': False, 'error': 'Something Went Wrong'}, status=500)
	return JsonResponse({'success': False, 'error': 'Method Not Allowed'}, status=405)