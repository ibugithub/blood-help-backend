from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import DonorProfile 
from django.contrib.auth import get_user_model
from .models import DonorProfile

class DonorSignUpForm(UserCreationForm):
  class Meta:
    model = get_user_model()
    fields = ['email', 'password1', 'password2']

  def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    user.set_password(self.cleaned_data['password1'])

    if commit:
      user.save()

class DonorProfileForm(forms.ModelForm):
  class Meta:
    model = DonorProfile
    fields = ['blood_type', 'rh_factor', 'contact', 'address']
