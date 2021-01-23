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
    if mid=='logout/':
        return user_logout(request)

    context = {
        'movie': Movie.objects.get(id=mid),
        'tickets': Screening.objects.filter(movie__id=mid).filter(screenDate__gte=now()).order_by('screenDate')[0:5]
    }
    return render(request, "movie.html", context)


def movie_screenings(request,sid):
    if sid=='logout/':
        return user_logout(request)
    context={
        'screenings': Screening.objects.filter(movie__id=sid).filter(screenDate__gte=now()).order_by('screenDate')
    }
    context['name'] = context['screenings'][0].movie.name
    return render(request, "screenings.html", context)


def movie_tickets(request,sid):
    if sid == 'logout/':
        return user_logout(request)

    if request.POST: #create new tickets and change img to seats
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


def cart(request):
    print(0)
    context = {
        'user_tickets': Ticket.objects.filter(user=request.user.id).filter(isTemp=True),
        'total': 0
    }
    for t in context['user_tickets']:
        context['total'] += t.screening.price
    return render(request, "cart.html", context)


def user_login(request):
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
        print("getting here all the time")
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login.html',{})


def user_logout(request):
    if request.POST:
        if 'logout' in request.POST.keys():
            logout(request)
    return redirect("/")

def payment(request,total,ticketList):
    if request.POST:
        for ticket in ticketList:
            ticket.isTemp=false
    return render(request,'payment.html',{'total':total,'ticketList':ticketList})

