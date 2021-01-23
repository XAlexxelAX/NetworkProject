import math

from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render, redirect
from movies.models import Movie, Screening, Ticket
from django.utils.timezone import now
from django.template.defaulttags import register
from django.contrib.auth import authenticate, login, logout
from verify_email.email_handler import send_verification_email
from django.contrib.auth.models import User

@register.filter
#function that returns the dict[key] in django template
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def division(value, arg):
    if arg!=0:
        return value / arg
    return 0

@register.filter
def sub(value, arg):
    return round(value - arg,2)
# Create your views here.


def home_view(request):
    context = {}
    context['movies'] = dict(sorted({movie.id: movie for movie in Movie.objects.all()}
                                    .items(), key=lambda item: item[1].rate, reverse=True)[0:7])
    context['screenings'] = dict(sorted({screening.id: screening for screening in Screening.objects.filter(screenDate__gt=now())}
                                    .items(), key=lambda item: item[1].screenDate)[0:7])
    return render(request, 'home.html', context)


def movie_detail(request, mid):
    context = {
        'movie': Movie.objects.get(id=mid),
        'tickets': Screening.objects.filter(movie__id=mid).filter(screenDate__gte=now()).order_by('screenDate')[0:5],
        'isMovieWatched':False
    }
    if request.user.is_authenticated:
        for ticket in Ticket.objects.all():
           if request.user.id==ticket.user and int(ticket.screening.movie.id)==int(mid):
                context['isMovieWatched']=True

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
                    if request.user.is_authenticated:
                        Ticket.objects.create(screening=Screening.objects.get(id=sid),
                                          row=int(seat[1]), seat=int(seat[2]),
                                          isTemp=True, user=request.user.id)
                    else:
                        t=Ticket.objects.create(screening=Screening.objects.get(id=sid),
                                          row=int(seat[1]), seat=int(seat[2]),
                                          isTemp=True, user=-1)
                        return payment(request, round(t.screening.price-t.screening.movie.salePrec*t.screening.price/100,2),[t])
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
    context = {'screenings': {},'sorting':'rate'}
    context['movies'] = {movie.id:movie for movie in Movie.objects.all()}
    for movie in context['movies']:
        context['screenings'][movie] = Screening.objects.filter(movie__id=movie).filter(screenDate__gte=now()).order_by('screenDate')[0:5]
    if request.POST:
        genresList=[]
        print(request.POST)
        if 'sortby' in request.POST:
            if request.POST['sortby'] == 'rate':
                if 'sorting' in request.POST and request.POST['sorting'] == 'asc':
                    context['movies'] = dict(sorted(context['movies']
                                                    .items(), key=lambda item: item[1].rate))
                else:
                    context['movies'] = dict(sorted(context['movies']
                                                    .items(), key=lambda item: item[1].rate, reverse=True))
            elif request.POST['sortby'] == 'price':
                if 'sorting' in request.POST and request.POST['sorting'] == 'asc':
                    context['movies'] = dict(sorted(context['movies'].items()
                                                    , key=lambda item: min([math.inf]+[s.price for s in Screening.objects.filter(movie__id=item[0])])))
                else:
                    context['movies'] = dict(sorted(context['movies'].items()
                                                    , key=lambda item: min([math.inf]+[s.price for s in Screening.objects.filter(movie__id=item[0])]), reverse=True))
            elif request.POST['sortby'] =='abc':
                if 'sorting' in request.POST and request.POST['sorting'] == 'asc':
                    context['movies'] = dict(sorted(context['movies']
                                                    .items(), key=lambda item: item[1].name))
                else:
                    context['movies'] = dict(sorted(context['movies']
                                                    .items(), key=lambda item: item[1].name, reverse=True))
        for r in request.POST:
            if 'genres' in r:
                genresList.append(r.split('_')[1].lower())
        if genresList:
            cpyDict = context['movies'].copy()
            for m in cpyDict:
                m_genre_list = context['movies'][m].genres.lower().replace(' ', '').split(',')
                if not set(set(genresList) & set(m_genre_list)):
                    context['movies'].pop(m)
    else:
        context['movies'] = dict(sorted(context['movies']
                                        .items(), key=lambda item: item[1].rate, reverse=True))
    return render(request, 'movieGallery.html', context)


def cart(request):
    context = {'total': 0}
    if request.POST:
        if 'remove' in request.POST:
            Ticket.objects.get(id=int(request.POST['remove'])).delete()
        if 'purchase' in request.POST:
            ticketList=[]
            total = 0
            for t in request.POST:
                if 'ticket' in t:
                    ticket = Ticket.objects.get(id=int(t.split('_')[1]))
                    ticketList.append(ticket)
                    total += ticket.screening.price
            if total > 0:
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

def user_register(request):
    if request.POST:
            User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    return render(request,'register.html',{})

def payment(request, total, ticketList):
    print("payment"+str(ticketList))
    print("payment"+str(request.POST))
    if request.POST:
        for ticket in ticketList:
            ticket.isTemp = False
            ticket.save()
    return render(request, 'payment.html', {'total': total, 'ticketList': ticketList})

