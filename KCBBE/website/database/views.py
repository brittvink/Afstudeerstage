from django.shortcuts import render
from .models import Information
from django.db import connection


# Create your views here.
def home(request):
    return render(request, 'home.html')

def titles(request):
    title_list = Information.objects.all()
    return render(request, 'title_list.html', {'title_list': title_list})