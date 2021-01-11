from django.urls import path

from . import views

urlpatterns = [
    path('alex', views.index, name='index'),
    path('', views.index, name='index'),
    path('tickets', views.tickets, name='tickets'),
]
