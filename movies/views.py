from django.http import HttpResponse
from django.shortcuts import render
from movies.models import Movie, Screening


# Create your views here.

def home_view(request):
    context = {
        'movies': {}
    }
    context['movies'] = dict(sorted({movie.id: movie for movie in Movie.objects.all()}.items(), key=lambda item: item[1].rate,reverse=True))
    return render(request, 'home.html', context)


def movie_detail(request, mid):
    context = {
        'movie': Movie.objects.get(id = mid),
        'tickets': Screening.objects.filter(movie__id = mid).filter(relevant=True).order_by('screenDate')[0:5]
    }
    return render(request, "movie.html", context)

def movie_ticket(request,mid):
    context={}
    return render(request, "ticket.html", context)


def movie_view(request):
    return render(request, 'movie.html', {})
