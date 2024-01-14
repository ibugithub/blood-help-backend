from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import DonorSignUpForm
from .forms import DonorProfileForm
from .models import DonorProfile

# Create your views here.
def hello_view(request):
  return render(request, 'home.html')

def donor_signup(request):
  if request.method == 'POST':
    print('the request is submitted')
    form = DonorSignUpForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')

  else:
    form = DonorSignUpForm()
  return render(request, 'donor_signup.html', {'form' : form})


def DonorProfileView(request):

  try:
    print('I am in try block')
    donor_profile = DonorProfile.objects.get(user=request.user)
    form = DonorProfileForm(instance=donor_profile)
    print('the donor profile is ',donor_profile)
    print('the donor profile form is', form)
  except DonorProfile.DoesNotExist:
    print("I am in the except block")
    form = DonorProfileForm()

  if request.method == 'POST':
    form = DonorProfileForm(request.POST, instance=donor_profile)
    if form.is_valid():
      donor_profile = form.save(commit=False)
      donor_profile.user = request.user
      donor_profile.save()
      return redirect('dashboard')
  return render(request, 'dashboard.html', {'form': form})
