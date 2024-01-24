from django.contrib.auth.models import BaseUserManager 
from django.core.exceptions import ValidationError 
from django.core.validators import validate_email 
from django.utils.translation import gettext_lazy as _ 


class UserManager(BaseUserManager):
  def email_validator(self, email):
    try:
      validate_email(email)
    except ValidationError:
      raise ValueError(_("Please enter a valid email address")) 
    

  def create_user(self, email, first_name, last_name, password=None, **extra_fields):
    print('create user has been called')
    if email:
      email = self.normalize_email(email)
      self.email_validator(email)
    else:
      raise ValueError('email must be specified')
    user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user  
  
  def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
    print('create super user has been called')
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_verified', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError(_("is_stafff must be true for admin users"))
    
    if extra_fields.get('is_superuser') is not True:
      raise ValueError(_("is_superuser must be true for admin users"))
    user = self.create_user(email, first_name, last_name, password, **extra_fields)
    return user