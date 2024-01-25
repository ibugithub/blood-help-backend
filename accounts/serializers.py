from rest_framework import serializers
from .models import User 


class UserRegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(max_length=68, min_length=6, write_only=True )
  password2 = serializers.CharField(max_length=68, min_length=6, write_only=True )

  class Meta:
    model = User
    fields=['email', 'password', 'password2'] 
  
  def validate(self, attrs):
    return super(UserRegisterSerializer, self).validate(attrs)
  
  def create(self, validated_data):
    return super(UserRegisterSerializer, self).create(validated_data)