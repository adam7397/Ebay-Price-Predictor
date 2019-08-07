from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search", views.search, name="search"),
    path("save", views.save, name="save"),
    path("savedsearch/<int:search_id>", views.savedsearch, name="savedsearch"),
    path("recentsearch/<int:search_id>", views.recentsearch, name="recentsearch")
]

# /<str:query> Needed?