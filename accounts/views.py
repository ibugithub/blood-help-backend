from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import DonorSignUpForm
from .forms import DonorProfileForm
from .models import DonorProfile
from allauth.account.views import LoginView
# Create your views here.
def hello_view(request):
  return render(request, 'home.html')

class LoginApi(LoginView):
  print('Hello world I am in the loginApi class')
  def dispatch(self, request, *args, **kwargs):
      print('I am the dispatch method in the LoginApi subclass')
      return super(LoginApi, self).dispatch(request, *args, **kwargs)
  print('I am at the bottom of the dispatch method')

  def form_valid(self, form):
    print('I am in form valid method')


def DonorProfileView(request): 
  donor_profile, created = DonorProfile.objects.get_or_create(user=request.user)
  form = DonorProfileForm(instance=donor_profile)
  if request.method == 'POST':
    form = DonorProfileForm(request.POST, instance=donor_profile)
    if form.is_valid():
      donor_profile = form.save(commit=False)
      donor_profile.user = request.user
      donor_profile.save()
      return redirect('dashboard')
  return render(request, 'dashboard.html', {'form': form})
