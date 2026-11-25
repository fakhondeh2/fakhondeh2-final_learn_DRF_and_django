from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def shop_index(request):
    context = {}
    return HttpResponse("<h1>my shop</h1>")