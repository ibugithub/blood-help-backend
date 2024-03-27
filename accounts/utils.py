import random 
from .models import User, UserOtp
from django.conf import settings
from django.core.mail import EmailMessage


def generateOtp():
  otp = ""
  for i in range(6):
    otp += str(random.randint(0,9))
  return otp

def send_code_to_user(userEmail):
  Subject = "One time passcode for email verification"
  passcode = generateOtp()
  user = User.objects.get(email=userEmail)
  current_site = 'blood-help'
  email_body = f"Hey {user.first_name} thanks for registering on {current_site}. Please verify your email with the following passcode {passcode}" 
  from_email = settings.DEFAULT_FROM_EMAIL
  UserOtp.objects.create(user=user, otp_code=passcode)
  email = EmailMessage(subject=Subject, body = email_body, from_email=from_email, to=[userEmail])
  email.send(fail_silently=True)

def send_email(data):
  email = EmailMessage(
    subject=data['email_subject'],
    body=data['email_body'],
    from_email=settings.EMAIL_HOST_USER,
    to=[data['to_email']]
  )
  email.send()
