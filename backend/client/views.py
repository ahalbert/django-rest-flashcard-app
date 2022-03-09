from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

import os
# books/views.py
from django.views.generic import ListView
# from .models import Book

def appView(request):
    return render(request,'index.html', {})
# Create your views here.
