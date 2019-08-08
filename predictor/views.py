from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import saved, recent, category
from predictor.prediction import *

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {'message': None})
    
    context = get_context(request)
    return render(request, "home.html", context)

def register(request):
    username = request.POST["username"]
    password = request.POST["password"]
    firstName = request.POST["firstName"]
    lastName = request.POST["lastName"]
    email = request.POST["email"]
    
    user = User.objects.create_user(username, email, password)
    user.first_name = firstName
    user.last_name = lastName
    user.save()
    
    # context = get_context(request)
    return render(request, "login.html", {'message': "Registered! Please log in"})

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return render(request, "home.html", get_context(request))
    else:
        return render(request, "login.html", {'message': "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "login.html", {'message': "Logged out."})

def search(request):
    term = request.POST["search_term"]
    categorystring = request.POST["category"]
    saverecent(request, term, categorystring)

    return render(request, "search.html", lookup(request, term, categorystring))

def savedsearch(request, search_id):
    search = saved.objects.get(id=search_id)
    saverecent(request, search.term, search.category.categoryId)

    return render(request, "search.html", lookup(request, search.term, search.category.categoryId))

# This method is identical to the saved search except for which table it queries
def recentsearch(request, search_id):
    search = recent.objects.get(id=search_id)
    saverecent(request, search.term, search.category.categoryId)

    return render(request, "search.html", lookup(request, search.term, search.category.categoryId))

# Created this helper function since there are two ways to search
def lookup(request, term, categorystring):
    plot, prediction, mean = webcall(term, categorystring)

    context = {
        'term': term,
        'category': categorystring,
        'plot': plot,
        'prediction': prediction,
        'average': mean
    }

    return context

# Created this helper function to take it out of lookup and make it useful for the save function too
# I call it cateogorystring to not conflict with the category table
def saverecent(request, term, categorystring):
    recent_search = recent(userid=request.user, term=term, category=category.objects.get(categoryId=categorystring))
    recent_search.save()

def save(request):
    # The hidden fields save me from query the database again to get the searched terms & category
    term = request.POST["term"]
    categorystring = request.POST["category"]

    new_save = saved(userid=request.user, term=term, category=category.objects.get(categoryId=categorystring))
    new_save.save()

    return render(request, "search.html", lookup(request, term, categorystring))

def get_context(request):
    # 10 return recent searches and other user data needed from the database
    # .distinct() with a positional argument only works with PostgreSQL, otherwise I would elminate seeing duplicates
    context = {
        'user': request.user,
        'saved_search': saved.objects.all().filter(userid=request.user.id),
        'categories': category.objects.all(),
        'recent': recent.objects.all().filter(userid=request.user.id).order_by('-id')[:10]
    }

    return context