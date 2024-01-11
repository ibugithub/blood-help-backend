from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import DonorSignUpForm
from allauth.account.views import LoginView
from allauth.account.forms import LoginForm

# Create your views here.
def hello_view(request):
  return render(request, 'home.html')

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

class CustomLoginView(LoginView):
  form_class = LoginForm
  print('I am here at main view')

  def form_invalid(self, form):
    print('I am here at the form')
    response = super().form_invalid(form)

    username_error = form.errors.get('username', None)
    password_error = form.errors.get('password', None)

    response.context_data['username_error'] = username_error
    response.context_data['password_error'] = password_error

    return response