from rest_framework import serializers
from .models import User 
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class UserRegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=68, min_length=6, write_only=True )
  password2 = serializers.CharField(max_length=68, min_length=6, write_only=True )

  class Meta:
    model = User
    fields=['email', 'first_name', 'last_name', 'password', 'password2'] 
  
  def validate(self, attrs):
    password = attrs.get('password', '')
    password2 = attrs.get('password2', '')
    if password != password2:
      raise serializers.ValidationError("Password do not match.")
    return attrs
  
  def create(self, validated_data):
    user = User.objects.create_user(
      email = validated_data['email'],
      password = validated_data['password'],
      first_name = validated_data['first_name'],
      last_name = validated_data['last_name']
    )
    return user
  

class LoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField( max_length=55 )
  password = serializers.CharField( max_length=60, write_only=True )
  access_token = serializers.CharField( max_length=255, read_only=True )
  refresh_token = serializers.CharField( max_length=255, read_only=True )
  class Meta:
    model=User
    fields=['email','full_name', 'password', 'access_token', 'refresh_token']

  def validate( self, attrs ):
    email = attrs.get('email')
    password = attrs.get('password')
    request = self.context.get('request')
    user = authenticate(request, email=email, password = password )

    if not user:
      raise AuthenticationFailed("Invalid user credentials") 
    
    if not user.is_verified:
      raise AuthenticationFailed("The Email isn't verified") 
    
    token = user.user_token()

    return {
      'email' : user.email,
      'full_name' : user.full_name,
      'access_token' : str(token.get('access')),
      'refresh_token' : str(token.get('refresh')),
    }
    