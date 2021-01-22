from django.http import HttpResponse
from django.shortcuts import render
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
    if request.POST: #create new tickets and change color to
        if 'logout' in request.POST.keys():
            django.contrib.auth.logout()
    print(request.POST)
    context = {}
    context['movies'] = dict(sorted({movie.id: movie for movie in Movie.objects.all()}.items(), key=lambda item: item[1].rate, reverse=True))
    return render(request, 'home.html', context)


def movie_detail(request, mid):
    if request.POST:  # create new tickets and change color to
        if 'logout' in request.POST.keys():
            django.contrib.auth.logout()

    context = {
        'movie': Movie.objects.get(id=mid),
        'tickets': Screening.objects.filter(movie__id=mid).filter(screenDate__gte=now()).order_by('screenDate')[0:5]
    }
    return render(request, "movie.html", context)

def movie_screenings(request,sid):
    if request.POST:  # create new tickets and change color to
        if 'logout' in request.POST.keys():
            django.contrib.auth.logout()

    context={
        'screenings': Screening.objects.filter(movie__id=sid).filter(screenDate__gte=now()).order_by('screenDate')
    }
    context['name'] = context['screenings'][0].movie.name
    return render(request, "screenings.html", context)

def movie_tickets(request,sid):
    if request.POST: #create new tickets and change img to seats
        for item in request.POST.keys():
            if 'seat' in item:
                Ticket.objects.create(screening=Screening.objects.get(id=sid),row=int(item[5]),seat=int(item[7]),isTemp=True,
                                      user=request.user.id)
            elif 'logout' in request.POST.keys():
                django.contrib.auth.logout()

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
    if request.POST:  # create new tickets and change color to
        if 'logout' in request.POST.keys():
            django.contrib.auth.logout()
    return render(request, 'movie.html', {})

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
            return render(request, 'ecommerce/user/account.html')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'ecommerce/user/login.html', {'error_message': 'Incorrect username and / or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        return render(request, 'login.html',{})

