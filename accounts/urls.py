from django.urls import path 
from . import views
from allauth.account.views import SignupView, LoginView


urlpatterns = [
  path('', views.hello_view, name='home'),
  path ('signup/', SignupView.as_view(), name='signup'),
  path('accounts/login/', views.LoginApi.as_view(), name='login'),
  path ('accounts/dashboard/', views.DonorProfileView, name='dashboard'),
  path('api/register/', views.RegisterUserView.as_view(), name='restR'),
  path('api/verify-email/', views.VerifyEmailView.as_view(), name='verifyEmail'),
  path ('api/login/', views.LoginApiView.as_view(), name='loginn'),
  path ('api/testAuth/', views.TestAuthenticationView.as_view(), name='testAuth'),
  path ('api/reset-password/', views.PasswordResetView.as_view(),  name='reset-password'),
  path ('api/reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='reset-password-confirm'),
  path ('api/set-new-password/', views.SetNewPassword.as_view(), name='set-new-password'),
  path('api/logout/', views.LogoutView.as_view(), name='Logout')
]