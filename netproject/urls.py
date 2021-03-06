"""netproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from movies import views as movies_views
from django.conf.urls import url

urlpatterns = [
    url(r'.*logout/', movies_views.user_logout, name='user_logout'),
    path('home/movie/', movies_views.movie_view, name='movie'),
    path('movies/', movies_views.movie_view, name='movies'),
    url(r'^movies/(?P<mid>.*)', movies_views.movie_detail, name='movie_detail'),
    url(r'^screenings/(?P<sid>.*)', movies_views.movie_screenings, name='movie_screenings'),
    url(r'^tickets/(?P<sid>.*)', movies_views.movie_tickets, name='movie_tickets'),
    path('admin/', admin.site.urls, name='admin'),
    path('', movies_views.home_view, name='home'),
    #path('verification/', include('verify_email.urls')),
    path('login/', movies_views.user_login, name='user_login'),
    path('register/', movies_views.user_register, name='user_register'),
    path('payment/', movies_views.payment, name='payment'),
    path('cart/', movies_views.cart, name='cart'),
    url(r'.*', lambda request: render(request, '404.html'), name='404'),
]
