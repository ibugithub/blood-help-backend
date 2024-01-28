from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import DonorProfileForm
from .models import DonorProfile
from allauth.account.views import LoginView
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import UserOtp
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


class RegisterUserView(GenericAPIView):
  serializer_class = UserRegisterSerializer

  def post(self, request): 
    print("i'm in the post method")
    user_data = request.data
    print("user data is", user_data)
    serializer = self.serializer_class(data = user_data)
    print("serializer is", serializer)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      user = serializer.data
      send_code_to_user(user['email'])
      return Response ({
        'data': user,
        'message': f"{user['first_name']} {user['last_name']} Thanks for registering"
      }, status = status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
  

class VerifyEmailView(GenericAPIView):
  def post(self, request):
    otpCode = request.data.get('otpCode')
    print('the otpCode', otpCode)
    try:
      user_code_obj = UserOtp.objects.get(otp_code = otpCode)
      print('the user_code_obj is', user_code_obj)
      user = user_code_obj.user
      print('the user', user)
      if not user.is_verified:
        user.is_verified = True
        user.save()
        return Response({
          'message' : 'account email verified successfully'
        }, status = status.HTTP_200_OK) 
      return Response({
        'message' : 'code is invalid user already verified' 
      }, status = status.HTTP_204_NO_CONTENT)
    except UserOtp.DoesNotExist:
      return Response({ 'message' : 'passcode does not exist' }, status = status.HTTP_404_NOT_FOUND)