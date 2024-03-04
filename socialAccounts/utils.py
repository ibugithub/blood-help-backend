from google.auth.transport import requests
from google.oauth2 import id_token 
from django.contrib.auth import authenticate 
from rest_framework.exceptions import  AuthenticationFailed
from django.conf import settings
from accounts.models import User


class Google():
  @staticmethod
  def validate(access_token):
    try:
      id_info = id_token.verify_oauth2_token(access_token, requests.Request())
      if 'accounts.google.com' in id_info['iss']:
        return id_info 
    except Exception as e: 
      return "token is invalid or has expired" 

def login_social_user(email, password):
  login_user=authenticate(email=email, password=password)
  user_tokens=login_user.user_token()
  return {
      'email': login_user.email,
      'full_name' : login_user.full_name,
      'access_token' : str(user_tokens.get('access')),
      'refresh_token' : str(user_tokens.get('refresh')),
  }

def register_social_user(provider, email, first_name, last_name):
  user = User.objects.filter(email=email) 
  if user.exists():
    if user[0].auth_provider == provider:
      login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)
    else:
      raise AuthenticationFailed(
        detail=f"Please login in with {user[0].auth_provider}"
      )
  else:
    new_user ={
      'email': email,
      'first_name': first_name,
      'last_name': last_name,
      'password': settings.SOCIAL_AUTH_PASSWORD
    }
    registered_user=User.objects.create(**new_user)
    registered_user.provider=provider
    registered_user.is_verified=True
    registered_user.save()
    login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)