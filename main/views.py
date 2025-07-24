from django.shortcuts import render

# Create your views here.
# main/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')
