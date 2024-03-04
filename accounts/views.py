from django.shortcuts import render, redirect
from django.shortcuts import render
from .forms import DonorProfileForm
from .models import DonorProfile, User
from allauth.account.views import LoginView
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, LoginSerializer, PasswordResetSerializer, SetNewPasswordSerializer, LogoutSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import UserOtp
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
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
    user_data = request.data
    serializer = self.serializer_class(data = user_data)
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
    try:
      user_code_obj = UserOtp.objects.get(otp_code = otpCode)
      user = user_code_obj.user
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

class LoginApiView(GenericAPIView):
  serializer_class = LoginSerializer
  def post(self, request):
    serializer = self.serializer_class(data = request.data, context= {'request': request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
class TestAuthenticationView(GenericAPIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    data = {
      'msg': "The request is authenticated"
    }
    return Response(data, status  = status.HTTP_200_OK) 
  
class PasswordResetView(GenericAPIView):
  serializer_class = PasswordResetSerializer 
  def post(self, request):
    serializer = self.serializer_class(data = request.data, context = {'request': request})
    serializer.is_valid(raise_exception=True)
    return Response({"message" : "A link has been sent to reset your password"}, status = status.HTTP_200_OK) 
  
class PasswordResetConfirm(GenericAPIView): 
  def get(self, request, uidb64, token):
    try:
      user_id = smart_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(id = user_id)
      if not PasswordResetTokenGenerator().check_token(user, token): 
        return Response({"message": "Token has invalid or has expired"}, status=status.HTTP_401_UNAUTHORIZED)
      return Response({"success": True, "messages": "Credentials is valid", "uidb64": uidb64, "token": token}, status=status.HTTP_200_OK)
    
    except DjangoUnicodeDecodeError:
      return Response({"message": "Token has invalid or has expired"}, status=status.HTTP_401_UNAUTHORIZED) 

class SetNewPassword(GenericAPIView):
  serializer_class = SetNewPasswordSerializer 
  def patch(self, request):
    serializer = self.serializer_class(data=request.data) 
    serializer.is_valid(raise_exception=True)
    return Response({"message": "password Reset done"}, status=status.HTTP_200_OK)
     
class LogoutView(GenericAPIView):
  serializer_class = LogoutSerializer 
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = self.serializer_class(data=request.data) 
    serializer.is_valid(raise_exception=True) 
    serializer.save() 
    return Response(status=status.HTTP_204_NO_CONTENT)