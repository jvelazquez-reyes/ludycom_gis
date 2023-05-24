from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import GeoLocalizer

from .forms import GeoLocalizerForm
from .geolocalizer import get_places

# Create your views here.

# Signup module
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('petitions')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

# Signin module
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('petitions')

# Create new search
@login_required
def create_petition(request):
    if request.method == "GET":
        return render(request, 'create_petition.html', {"form": GeoLocalizerForm})
    else:
        try:
            longitude = float(request.POST["longitude"])
            latitude = float(request.POST["latitude"])

            nearby_places = get_places(longitude, latitude)

            for place_found in range(len(nearby_places)):
                form = GeoLocalizerForm(request.POST)
                new_petition = form.save(commit=False)
                new_petition.place = nearby_places[place_found][0]
                new_petition.name = nearby_places[place_found][1]
                new_petition.distance = nearby_places[place_found][4]
                new_petition.user = request.user
                new_petition.save()

            return redirect('petitions')
        except ValueError:
            return render(request, 'create_petition.html', {"form": GeoLocalizerForm, "error": "Error creating task."})

# Get all found nearby places filtered by authenticated user
@login_required
def petitions(request):
    petitions = GeoLocalizer.objects.filter(user=request.user)
    return render(request, 'petitions.html', {"petitions": petitions})

# Get the details of each found nearby place
@login_required
def petition_detail(request, petition_id):
    if request.method == 'GET':
        petition = get_object_or_404(GeoLocalizer, pk=petition_id, user=request.user)
        form = GeoLocalizerForm(instance=petition)
        return render(request, 'petition_detail.html', {'petition': petition, 'form': form})

# Home page
def home(request):
    return render(request, 'home.html')

# Signout module
@login_required
def signout(request):
    logout(request)
    return redirect('home')
