from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from .models import Book, Station, Trip, Seat
from django.core import serializers
import json

@never_cache
def home(request):
    trips = Trip.objects.all()
    temp = Trip.objects.values()
    stations = Station.objects.all()
    tripJSON = serializers.serialize("json",trips)
    tripObj = json.loads(tripJSON)
    return render(request, 'sitePages/home.html', {'trips': trips, 'stations': stations, 'data': json.dumps(list(tripObj))})


@never_cache
def signIn(request):
    return render(request, 'registrationPages/signIn.html')


@never_cache
def signUp(request):
    return render(request, 'registrationPages/SignUp.html')


@never_cache
def signUpForm(request):
    template = 'registrationPages/signUp.html'

    form = request.POST
    if User.objects.filter(username=request.POST.get('username')).exists():
        return render(request, template, {'form': form, 'errorMsg': 'Username is already taken.'})

    elif User.objects.filter(email=request.POST.get('email')).exists():
        return render(request, template, {'form': form, 'errorMsg': 'Email already exists.'})

    else:
        if request.method == "POST":
            user = User.objects.create_user(
                request.POST.get('username'),
                request.POST.get('email'),
                request.POST.get('pass')
            )
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            if request.POST.get('isAdmin') == "true":
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
            user.save()
            
            login(request, user)
            return redirect('/')
    


def signInForm(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
        else:
            return render(request, 'registrationPages/signIn.html', {'errorMsg': 'Wrong username or password'})



def logOut(request):
    request.session.flush()
    return redirect('/')

def updateProfile(request, username):
    form=request.POST
    template='sitePages/profile.html'
    user=User.objects.filter(username=username)
    if user.username!=request.POST.get('uname'):
        if User.objects.filter(username=request.POST.get('uname')).exists():
            return render(request, template, {'form': form, 'errorMsg': 'Username is already taken.'})
        else:
            user.username=request.POST.get('uname')

    if user.email!=request.POST.get('email'):
        if User.objects.filter(email=request.POST.get('email')).exists():
            return render(request, template, {'form': form, 'errorMsg': 'Email is already taken.'})
        else:
            user.email=request.POST.get('email')
    if user.first_name!=request.POST.get('fname'): 
        user.first_name=request.POST.get('fname') 
    if user.last_name!=request.POST.get('lname'): 
        user.last_name=request.POST.get('lname')  
    if user.password!=request.POST.get('pass'): 
        user.password=request.POST.get('pass')       
    user.save()           


def profile(request, username):
    return render(request, "sitePages/profile.html", {'username': username})

def myTrips(request, id):
    book = Book.objects.filter(user = id)
    return render(request, "sitePages/myTrips.html", {'books': book})

def cancelBook(request):
    if request.is_ajax:
        if request.method =="GET":
            bookId = request.GET['bookId']
            userId = request.GET['userId']
            obj = Book.objects.filter(id=bookId)
            trip = obj[0].trip
            bookSeats = obj.values_list('seatTrain', flat=True)
            seatCount = len(bookSeats)
            trip.Remaining_seats += seatCount
            trip.save()
            obj.delete()   
            return myTrips(request, userId)

def certainTrip(request, id):
    if request.user.is_authenticated:
        trip = Trip.objects.get(id = id)

        return render(request, 'sitePages/certainTrip.html', {'trip': trip})
    else:
        trips = Trip.objects.all()
        return render(request, 'sitePages/home.html', {'errorMsg': 'Please sign in or sign up to book', 'trips': trips})

def book(request):
    if request.method == "POST":
        tid = request.POST.get('tripId')
        if(tid is None):
            return render
        trip = Trip.objects.get(id = tid)
        book = Book(
                trip = trip,
                user = request.user,
                seats = len(request.POST.get('selected')),
            )
        book.save()
        
        for i in request.POST.getlist('selected'):
            if not Seat.objects.filter(id = i):
                seat = Seat(id = i)
                seat.save()
            seat = Seat.objects.get(id = i)
            book.seatTrain.add(seat)
            trip.Remaining_seats -= 1
            trip.save()
        book.save()
        trips = Trip.objects.all()
        return render(request, 'sitePages/Home.html', {'errorMsg': 'Book is successful', 'trips': trips})
