from django.shortcuts import render
from django.http import response

# Create your views here.
def index(request):
    context = {}        
    return render(request, "index.html", context)