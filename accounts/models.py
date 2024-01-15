from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin 
from django.utils import timezone
from django.contrib.auth import get_user_model

# This is custom user manager class. It Will be used to create custom user
class UserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError('email must be specified')
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user  
  
  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email,password, **extra_fields)


# This is the custom User class 
class User(AbstractBaseUser, PermissionsMixin): 
  email = models.EmailField(unique=True)
  first_name = models.CharField(max_length=30 )
  last_name = models.CharField(max_length=30 )
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  date_joined = models.DateField(default=timezone.now)

  objects = UserManager() 
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  def __str__(self):
    return self.email

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

class DonorProfile(models.Model):
  user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE) 
  blood_type = models.CharField(max_length=15, choices=BLOOD_TYPES, blank=True, null=True)
  rh_factor = models.CharField(max_length=10, choices=RH_FACTOR, blank=True, null=True)
  contact = models.CharField(max_length=15, blank=True, null=True)
  address = models.TextField(blank=True, null=True)
  def __str__(self):
    return self.blood_type
