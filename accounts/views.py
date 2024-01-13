from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import DonorSignUpForm
from allauth.account.views import LoginView as DjangoLoginView
from allauth.account.forms import LoginForm
from django.http import HttpResponseBadRequest

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


class CustomLoginView(DjangoLoginView):
  print("I am in the custom Login veiw")
  def form_invalid(self, form):
    print("Invalid form submission. Errors:")
    print(form.errors)

    return HttpResponseBadRequest("Invalid form submission. Please check your credentials.")