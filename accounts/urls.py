from django.urls import path 
from . import views
from allauth.account.views import SignupView, LoginView


urlpatterns = [
  path('', views.hello_view, name='home'),
  path ('signup', SignupView.as_view(), name='signup'),
  path('accounts/login/', views.LoginApi.as_view(), name='login'),
  path ('accounts/dashboard/', views.DonorProfileView, name='dashboard'),
]