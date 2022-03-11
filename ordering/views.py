from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'ordering/index.html')

def about(request):
    return HttpResponse("We are at about")

def contact(request):
    return HttpResponse("We are at contact")