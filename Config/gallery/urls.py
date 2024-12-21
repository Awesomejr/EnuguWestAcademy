from django.urls import path, include
from . import views

app_name = "gallery"
urlpatterns = [
    path("", views.gallery, name="gallery"),
    path("create-gallery-category/", views.createGalleryCategory, name="createGalleryCategory"),
    path("create-gallery-event/", views.createGalleryEvent, name="createGalleryEvent"),
    path("edit-gallery-event/<uuid:eventId>/", views.editGalleryEvent, name="editGalleryEvent"),
    path("add-gallery-image/", views.addGalleryImage, name="addGalleryImage"),

    path("photo/<str:pk>/", views.viewImage, name="viewImage"),
]