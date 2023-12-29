from django.urls import path 
from . import views


urlpatterns = [
  path('', views.hello_view, name='home'),
  path ('signup', views.donor_signup, name='donor_signup')
]