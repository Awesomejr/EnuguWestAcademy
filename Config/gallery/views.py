import logging

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Event, EventImage, EventCategory
from .forms import GallerySearchForm, CreateGalleryCategoryForm, CreateGalleryEventForm, AddGalleryImageForm
from base.forms import LoginForm

from utilities import customFuncs

logger = logging.getLogger(__name__)

# Create your views here.
@login_required(login_url="base:home")
def createGalleryCategory(request):
    categories = EventCategory.objects.all()

    if request.method == "POST":
        form = CreateGalleryCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()

            logger.info(f"'{category.name}' category has been created successffully.")
            messages.success(request, f"'{category.name}' category has been created successffully.")
            return redirect("gallery:createGalleryCategory")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateGalleryCategoryForm()

    context = {"categories": categories, "form": form}
    return render(request, "./gallery/pages/createGalleryCategory.html", context=context)


@login_required(login_url="base:home")
def createGalleryEvent(request):
    events = Event.objects.select_related("category").prefetch_related("images").all()

    if request.method == "POST":
        form = CreateGalleryEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()

            logger.info(f"'{event.title}' event has been created successffully.")
            messages.success(request, f"'{event.title}' event has been created successffully.")
            return redirect("gallery:createGalleryEvent")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateGalleryEventForm()

    context = {"events": events, "form": form, "page_title": "Create Event"}
    return render(request, "./gallery/pages/createGalleryEvent.html", context=context)


@login_required(login_url="base:home")
def editGalleryEvent(request, eventId):
    events = Event.objects.select_related("category").prefetch_related("images").all()
    event = Event.objects.select_related("category").prefetch_related("images").get(id=eventId)

    if request.method == "POST":
        form = CreateGalleryEventForm(request.POST, instance=event)
        if form.is_valid():
            event_ = form.save(commit=False)
            event_.created_by = request.user
            event_.save()

            logger.info(f"'{event_.title}' event has been created successffully.")
            messages.success(request, f"'{event_.title}' event has been created successffully.")
            return redirect("gallery:createGalleryEvent")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = CreateGalleryEventForm(instance=event)

    context = {"events": events, "form": form, "page_title": "Edit Event"}
    return render(request, "./gallery/pages/createGalleryEvent.html", context=context)


@login_required(login_url="base:home")
def addGalleryImage(request):
    event_images = EventImage.objects.all()

    if request.method == "POST":
        form = AddGalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            event_image = form.save(commit=False)
            event_image.created_by = request.user
            event_image.save()

            logger.info(f"Event image has been added to '{event_image.event.title}' successffully.")
            messages.success(request, f"Event image has been added to '{event_image.event.title}' successffully.")
            return redirect("gallery:createGalleryEvent")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = AddGalleryImageForm()

    context = {"form": form, "event_images": event_images}
    return render(request, "./gallery/pages/addGalleryImage.html", context=context)


def gallery(request):
    category = request.GET.get("category")
    event_images = EventImage.objects.all()
    print(f"Category: {category}")

    if category == None:
        event_images = EventImage.objects.all() # Get all images
    else:
        event_images = EventImage.objects.filter(event__title=category)

    events = Event.objects.all()
    display_images = EventImage.objects.all().order_by("-created_on")[0:5]

    form = LoginForm()
    gallery_search_form = GallerySearchForm()

    context = {
            "events": events, "event_images": event_images, 
            "display_images": display_images, "form": form,
            "gallery_search_form": gallery_search_form
        }
    return render(request, "./gallery/pages/gallery.html", context=context)


def viewImage(request, pk):
    event_image = EventImage.objects.get(id=pk)
    return render(request, "./gallery/pages/viewImage.html", {"event_image": event_image})


