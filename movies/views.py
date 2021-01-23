from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render, redirect
from movies.models import Movie, Screening, Ticket
from django.utils.timezone import now
from django.template.defaulttags import register
from django.contrib.auth import authenticate, login, logout

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


def movie_tickets(request, sid):
    print(request.POST)
    if request.POST: #create new tickets and change img to seats
        for item in request.POST.keys():
            if 'seat' in item:
                seat = item.split('_')
                if request.POST[item] == 'add':
                    Ticket.objects.create(screening=Screening.objects.get(id=sid),
                                          row=int(seat[1]), seat=int(seat[2]),
                                          isTemp=True, user=request.user.id)
                elif request.POST[item] == 'remove':
                    ticketID = Ticket.objects.filter(screening__id=sid).filter(row=int(seat[1])).\
                                            filter(seat=int(seat[2]))[0].id
                    Ticket.objects.get(id=ticketID).delete()
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
    print(context['ticketDict'])
    return render(request, "tickets.html", context)


def movie_view(request):
    return render(request, 'movie.html', {})


def cart(request):
    context = {'total':0}
    if request.POST:
        print(request.POST)
        if 'remove' in request.POST:
            Ticket.objects.get(id=int(request.POST['remove'])).delete()
        if 'purchase' in request.POST and 'ticket' in request.POST:
            ticketList=[]
            total = 0
            for t in request.POST['ticket']:
                ticket = Ticket.objects.get(id=int(t))
                ticketList.append(ticket)
                total += ticket.screening.price
            return payment(request, total, ticketList)
    context['user_tickets'] = Ticket.objects.filter(user=request.user.id).filter(isTemp=True)
    for t in context['user_tickets']:
        context['total'] += t.screening.price
    return render(request, "cart.html", context)


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            return redirect("/")
        else:
            # Incorrect credentials, throw an error to the screen.
            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login.html',{})


def user_logout(request):
    if request.POST:
        if 'logout' in request.POST.keys():
            logout(request)
    return redirect("/")

