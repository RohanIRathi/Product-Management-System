from django.urls import re_path
from . import views

urlpatterns = [
	re_path(r"login\/?$", views.login, name="login"),
	re_path(r"signup\/?$", views.signup, name="signup"),
	re_path(r"getDistributorsList\/?$", views.get_distributors_list, name="fetch_distributors"),
	re_path(r"getAllRetailers\/?$", views.get_retailers_list, name="getAllRetailers"),
	re_path(r"getProfileDetails/<int:user_id>\/?$", views.get_profile_details, name="fetchProfileDetails"),
	re_path(r"verifyAccount\/?$", views.verify_account, name="verifyAccount"),
	re_path(r"changePassword\/?$", views.change_password, name="changePassword"),
	re_path(r"getRetailerDetails/<int:user_id>\/?$", views.get_retailer_details, name="getRetailerDetails"),
]