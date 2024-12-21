from django.urls import path, include
from . import views

app_name = "news"
urlpatterns = [
    path("", views.news, name="news"),
    path("events/", views.events, name="events"),
    path("create-news/", views.createNews, name="createNews"),
    path("event/create-event/", views.createEvent, name="createEvent"),
]