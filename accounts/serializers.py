from rest_framework import serializers
from .models import User 


class UserRegisterSerializer(serializers.ModelSerializer):
  print("i'm in the user register serializer")
  password = serializers.CharField(max_length=68, min_length=6, write_only=True )
  password2 = serializers.CharField(max_length=68, min_length=6, write_only=True )

  class Meta:
    model = User
    fields=['email', 'first_name', 'last_name', 'password', 'password2'] 
  
  def validate(self, attrs):
    print("i'm in the serializer's validate method")
    print("The attrs is ", attrs)
    password = attrs.get('password', '')
    password2 = attrs.get('password2', '')
    if password != password2:
      raise serializers.ValidationError("Password do not match.")
    return attrs
  
  def create(self, validated_data):
    print("i'm in the serializer's create method")
    print("The validated data  is ", validated_data)
    user = User.objects.create_user(
      email = validated_data['email'],
      password = validated_data['password'],
      first_name = validated_data['first_name'],
      last_name = validated_data['last_name']
    )
    return user