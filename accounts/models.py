from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 
from django.utils import timezone
from django.contrib.auth import get_user_model
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken



# This is the custom User class 
class User(AbstractBaseUser, PermissionsMixin): 
  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=30 )
  last_name = models.CharField(max_length=30 )
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  is_verified = models.BooleanField(default=False)
  date_joined = models.DateField(default=timezone.now)

  objects = UserManager() 
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['first_name', 'last_name']
  def __str__(self):
    return self.email
  
  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}" 
  
  def user_token(self):
    refresh = RefreshToken.for_user(self)
    return {
      'refresh' : str(refresh),
      'access' : str(refresh.access_token)
    }

BLOOD_TYPES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
]

RH_FACTOR = [
  ('POSITIVE', 'Positive'),
  ('NEGATIVE', 'Negative'),
]

GENDER = [
  ('MALE', 'MALE'),
  ('FEMALE', 'FEMALE'),
  ('OTHER', 'OTHER'),
]

class UserOtp(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  otp_code = models.CharField(max_length=6, unique=True )

  def __str__(self):
    return f"{self.user.email}--passcode"

class DonorProfile(models.Model):
  user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE) 
  blood_type = models.CharField(max_length=15, choices=BLOOD_TYPES, blank=True, null=True)
  rh_factor = models.CharField(max_length=10, choices=RH_FACTOR, blank=True, null=True)
  contact = models.CharField(max_length=15, blank=True, null=True)
  address = models.TextField(blank=True, null=True)
  def __str__(self):
    return self.blood_type


