from pickle import FALSE
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.contrib.auth.hashers import check_password

from .models import User

from email.mime.image import MIMEImage
import os
from datetime import datetime, timedelta
import pandas as pd
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

		try:
			send_request_email(request, user)
		except Exception as e:
			user.delete()
			return JsonResponse({'success': False, 'error': 'Something Went Wrong'}, status=500)

		return JsonResponse({"success": True, 'message': 'Your account has been created and is pending verification.'}, status=200)

	return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def send_request_email(request, user):
	url = str(request.META['HTTP_REFERER'])
	token = urlsafe_base64_encode(force_bytes(str(datetime.now()) + "~" + str(user.id)))
	url = url + 'verifyAccount?token=' + str(token)
	mail_details = {
		'verifyurl': url,
		'first_name': user.first_name,
		'last_name': user.last_name,
	}
	to_email = [user.Distributor.email]
	subject = "Request for Account Creation"
	html_message = render_to_string("registration/request-email.html", mail_details)
	message = strip_tags(html_message)
	from_email = settings.EMAIL_HOST_USER

	images = (("email/YashLogo.png", "logoImage"), ("email/banner2.png", "bannerImage"))

	msg = mail.EmailMultiAlternatives(subject, message, from_email, to_email)
	msg.attach_alternative(html_message, 'text/html')
	for image in images:
		with open(os.path.join(settings.MEDIA_ROOT, image[0]), "rb") as img:
			msgImage = MIMEImage(img.read())
			msgImage.add_header('Content-ID', f'<{image[1]}>')
			msg.attach(msgImage)
	msg.send()
    
    # mail.send_mail(subject, message, from_email, to_email, html_message=html_message, fail_silently=False)

def get_retailer_details(request, user_id=None):
	session_data = request.session.decode(request.headers['Session'])
	distributor = User.objects.get(pk=session_data['id'])
	if not distributor.is_superuser or not distributor.is_staff:
		return JsonResponse({'success': False, 'error': 'Action Unauthorized'}, status=401)
	try:
		retailer = User.objects.get(pk=user_id)
		return JsonResponse({'success': True, 'retailer': retailer.json()}, status=200)
	except User.DoesNotExist:
		return JsonResponse({'success': False, 'error': 'User not found'}, status=404)

def get_distributors_list(request):
	if request.method == "GET":
		distributors_list = User.objects.filter(is_superuser=True).filter(is_staff=True)
		response = [distributor.json() for distributor in distributors_list]
		return JsonResponse({'success': True, 'dist_list': response}, status=200)

def get_retailers_list(request):
	print(str(request.META['HTTP_REFERER'])+'verifyAccount?token=')
	if request.method == 'GET':
		session_data = request.headers['Session']
		user_id = request.session.decode(session_data)['id']
		current_user = User.objects.get(pk=user_id)
		if current_user.is_superuser and current_user.is_staff:
			retailers_list = User.objects.filter(Distributor=current_user).filter(is_superuser=False).filter(is_staff=True)
			response = [retailer.json() for retailer in retailers_list]
			return JsonResponse({'success': True, 'retailer_list': response}, status=200)

def get_profile_details(request, **kwargs):
	if request.method == 'GET':
		user_id = kwargs['user_id']
		try:
			user = User.objects.get(pk=user_id)
			if user.is_active:
				return JsonResponse({'success': True, 'user': user.json()}, status=200)
			else:
				return JsonResponse({'success': False, 'error': 'Account not verified'}, status=403)
		except User.DoesNotExist:
			return JsonResponse({'success': False, 'error': 'User Does Not Exist'}, status=400)
		except:
			return JsonResponse({'success': False, 'error': 'Something Went Wrong'}, status=500)

@csrf_exempt
def verify_account(request):
	session_data = request.session.decode(request.headers['Session'])
	try:
		distributor = User.objects.get(pk = session_data['id'])
		if not distributor.is_superuser and not distributor.is_staff:
			raise User.DoesNotExist()
	except User.DoesNotExist:
		return JsonResponse({'success': False, 'error': 'Action Unauthorized'}, status=403)
	token = request.GET['token']
	decoded = force_str(urlsafe_base64_decode(token))
	[token_datetime, id] = decoded.split('~')
	try:
		user = User.objects.get(pk=id)
		if user and datetime.now() < pd.to_datetime(token_datetime) + timedelta(days=7):
			if not user.is_active:
				if request.method == 'GET':
					return JsonResponse({'success': True, 'retailer': user.json()}, status=200)
				elif request.method == 'POST':
					body = json.loads(request.body)
					credit_limit = body['credit_limit']
					accept = body['accept']
					if not accept:
						user.delete()
						return JsonResponse({'success': True, 'message': 'User has been rejected and the account is deleted'}, status=200)
					else:
						user.is_active = True
						user.CreditLimit = credit_limit
						user.save()
						return JsonResponse({'success': True, 'message': 'User has been accepted and the credit limit is set'}, status=200)
			else:
				return JsonResponse({'success': False, 'error': 'The Retailer has already been accepted'}, status=400)
		elif user:
			user.delete()
			return JsonResponse({'success': False, 'error': 'Link expired'})
	except User.DoesNotExist:
		return JsonResponse({'success': False, 'error': 'No Such User to Validate!'}, status=401)
	return JsonResponse({'success': False, 'error': 'Method Not Allowed'}, status=405)

@csrf_exempt
def change_password(request):
	if request.method == 'POST':
		session_data = request.session.decode(request.headers['Session'])
		try:
			user = User.objects.get(pk=session_data['id'])
			data = json.loads(request.body)
			currentPassword = data['oldPassword']
			newPassword = data['newPassword']
			confirmPassword = data['confirmPassword']
			if not check_password(currentPassword, user.password):
				return JsonResponse({'success': False, 'error': 'The Current Password entered is incorrect'}, status=401)
			elif currentPassword == newPassword:
				return JsonResponse({'success': False, 'error': 'New Password cannot be the same as Current Password'}, status=400)
			elif newPassword == confirmPassword:
				user.set_password(newPassword)
				return JsonResponse({'success': True, 'message': 'Password Changed Successfully'}, status=200)
			else:
				return JsonResponse({'success': False, 'error': 'New Passwords Do Not Match'}, status=401)
		except User.DoesNotExist:
			return JsonResponse({'success': False, 'error': 'Something Went Wrong. Try logging in again.'}, status=400)