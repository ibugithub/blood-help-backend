from django.urls import path 
from . import views
from django.contrib.auth.views import LoginView


urlpatterns = [
  path('', views.hello_view, name='home'),
  path ('signup', views.donor_signup, name='donor_signup'),
  path('accounts/login/', LoginView.as_view(), name='login'),
  path ('accounts/dashboard/', views.DonorProfileView, name='dashboard'),
]