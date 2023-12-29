from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import DonorSignUpForm

# Create your views here.
def hello_view(request):
  return render(request, 'hello.html')

def donor_signup(request):
  if request.method == 'POST':
    print('the request is submitted')
    form = DonorSignUpForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('home')

  else:
    form = DonorSignUpForm()
  return render(request, 'donor_signup.html', {'form' : form})
