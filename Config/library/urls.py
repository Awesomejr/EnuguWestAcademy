from django.urls import path

from library import views

app_name = "library"
urlpatterns =[
    path("", views.books, name="books"),

    path("sort-class/", views.sortByClass, name="sortByClass"),
    path("sort-subject/", views.sortBySubject, name="sortBySubject"),
    path("sort-newest/", views.sortByNewest, name="sortByNewest"),
]