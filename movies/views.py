from django.http import HttpResponse
from django.shortcuts import render
from movies.models import Movie, Screening
from django.utils.timezone import now

# Create your views here.

def home_view(request):
    context = {}
    context['movies'] = dict(sorted({movie.id: movie for movie in Movie.objects.all()}.items(), key=lambda item: item[1].rate, reverse=True))
    return render(request, 'home.html', context)


def movie_detail(request, mid):
    context = {
        'movie': Movie.objects.get(id=mid),
        'tickets': Screening.objects.filter(movie__id=mid).filter(screenDate__gte=now()).order_by('screenDate')[0:5]
    }
    return render(request, "movie.html", context)

def movie_screenings(request,sid):
    context={
        'screenings': Screening.objects.filter(movie__id=sid).filter(screenDate__gte=now()).order_by('screenDate')
    }
    context['name'] = context['screenings'][0].movie.name
    return render(request, "screenings.html", context)

def movie_tickets(request,mid):
    context={}
    return render(request, "tickets.html", context)

def movie_view(request):
    return render(request, 'movie.html', {})
