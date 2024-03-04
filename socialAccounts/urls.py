from django.urls import path
from . import views 

urlpatterns=[
  path('api/google/', views.GoogleSignInView.as_view(), name='google')
]