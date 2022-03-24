from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login

from .models import User

import json

# Create your views here.

@csrf_exempt
def login(request):
	if request.method == "POST":
		data = json.loads(request.body)
		username = data['username']
		password = data['password']
		if User.objects.filter(username=username).exists():
			user = authenticate(request, username=username, password=password)
			if user:
				auth_login(request, user)
				userSession = request.session.create_model_instance(user.json())
				userSession.save()
				response = {
					'user': user.json(),
					'success': True,
					'session_key': userSession.session_key,
					'session_data': userSession.session_data,
				}
				return JsonResponse(response, status=200)
			return JsonResponse({'error': 'Incorrect Password', 'success': False}, status=401)
		return JsonResponse({'error': 'User Does not exist', 'success': False}, status=401)

@csrf_exempt
def signup(request):
	if request.method == "POST":
		data = json.loads(request.body)
		username = data['username']
		password1 = data['password1']
		password2 = data['password2']
		first_name = data['firstName']
		last_name = data['lastName']
		email = data['email']
		address = data['address']
		mobile = data['mobile']
		distributorId = data['distributorId']

		if password1 != password2:
			return JsonResponse({"success": False, "error": "Passwords do not match"}, status=400)
		check_existing = User.objects.filter(username=username)
		if check_existing.first():
			return JsonResponse({"success": False, "error": "Username taken"}, status=400)

		distributor = User.objects.filter(pk=distributorId).first()

		user = User(
					username=username,
					email=email,
					first_name=first_name,
					last_name=last_name,
					Address = address,
					Contact=mobile,
					Distributor=distributor,
					is_staff=True,
					is_active=False,
					is_superuser=False
				)
		user.set_password(password1)
		user.save()

		return JsonResponse({"success": True, 'message': 'Your account has been created and is pending verification.'}, status=200)

	return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def get_distributors_list(request):
	if request.method == "GET":
		distributors_list = User.objects.filter(is_superuser=True).filter(is_staff=True)
		response = [distributor.json() for distributor in distributors_list]
		return JsonResponse({'success': True, 'dist_list': response}, status=200)