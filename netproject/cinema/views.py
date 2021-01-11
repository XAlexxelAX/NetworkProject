from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


def index(request):
    HttpResponse('Blankovich')
    return HttpResponse("Shahar, it's alive!")


def tickets(request):
    return HttpResponse("Ticket Page.")
