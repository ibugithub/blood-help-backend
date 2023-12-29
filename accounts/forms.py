from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import DonorProfile 
from django.contrib.auth import get_user_model

class DonorSignUpForm(UserCreationForm):
  blood_type = forms.ChoiceField(choices=DonorProfile._meta.get_field('blood_type').choices)
  rh_factor = forms.ChoiceField(choices=DonorProfile._meta.get_field('rh_factor').choices)
  contact = forms.CharField(max_length=15)
  address = forms.CharField(widget=forms.Textarea)

  class Meta:
    model = get_user_model()
    fields = ['email', 'password1', 'password2', 'blood_type', 'rh_factor', 'contact', 'address' ]

  def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data['email']
    user.set_password(self.cleaned_data['password1'])

    if commit:
      user.save()

    DonorProfile.objects.create(
      user = user,
      blood_type=self.cleaned_data['blood_type'],
      rh_factor=self.cleaned_data['rh_factor'],
      contact=self.cleaned_data['contact'],
      address=self.cleaned_data['address']
    )