from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import saved, recent, category
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
    
    context = get_context(request)
    return render(request, "home.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "login.html", {"message": "Logged out."})

def search(request):
    term = request.POST["search_term"]
    category = request.POST["category"]

    context = {
        'term': term,
        'category': category
    }
    return render(request, "search.html", context)

def save(request):
    new_save = saved(userid = request.user.id, term = "NEED TERM", category = "NEED CATEGORY")

    return render(request, search.html, context)


def get_context(request):
    # Return recent searches and other user data needed from the database

    context = {
        'user': request.user,
        'saved_search': saved.objects.all().filter(userid=request.user.id),
        'categories': category.objects.all()
    }

    return context