from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    """Default index view that returns Hello World!"""
    return HttpResponse('<h1>Hello World!</h1>')
