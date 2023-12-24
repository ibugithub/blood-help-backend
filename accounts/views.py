from django.shortcuts import render
from django.http import JsonResponse 
from django.shortcuts import render

# Create your views here.
def hello_view(request):
  return render(request, 'hello.html')