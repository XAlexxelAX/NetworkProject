from django.http import HttpResponse
from django.shortcuts import render
from movies.models import Movie, Screening, Ticket
from django.utils.timezone import now
from django.template.defaulttags import register

@register.filter
#function that returns the dict[key] in django template
def get_item(dictionary, key):
    return dictionary.get(key)

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

def movie_tickets(request,sid):
    if request.POST: #create new tickets and change color to
        for item in request.POST.keys():
            if 'seat' in item:
                Ticket.objects.create(screening=Screening.objects.get(id=sid),row=int(item[5]),seat=int(item[7]),isTemp=True,
                                      user=request.user.id)


    context={}
    context['screening'] = Screening.objects.get(id=sid)
    context['ticketDict'] = {}
    for ticket in Ticket.objects.filter(screening__id=sid):
        try:#{1:{2:ticket, 10:ticket},15:{5:ticket,17:ticket}}
            context['ticketDict'][ticket.row][ticket.seat]=ticket
        except:
            context['ticketDict'][ticket.row]={}
            context['ticketDict'][ticket.row][ticket.seat] = ticket
    context['rows'] = range(context['screening'].hall.rows)
    context['seats'] = range(context['screening'].hall.columns)
    context['name'] = context['screening'].movie.name
    return render(request, "tickets.html", context)

def movie_view(request):
    return render(request, 'movie.html', {})



