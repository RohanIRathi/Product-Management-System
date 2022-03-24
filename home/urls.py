from django.urls import path
from . import views

urlpatterns = [
	path("login/", views.login, name="login"),
	path("signup/", views.signup, name="signup"),
	path("getDistributorsList/", views.get_distributors_list, name="fetch_distributors"),
]
