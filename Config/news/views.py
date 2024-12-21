import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required

from .models import Events, News
from .forms import NewsCreationsForm, EventCreationForm
from base.forms import LoginForm
from base.models import Session
from utilities.customFuncs import displayFormErrors, resizeImage


logger = logging.getLogger(__name__)

# Create your views here.
def news(request):
    all_news = News.objects.all()
    form = LoginForm()

    return render(request, "./news/pages/news.html", {"all_news": all_news, "form": form})

def events(request):
    events = Events.objects.all().order_by("-created_on")
    form = LoginForm()

    return render(request, "./news/pages/events.html", {"events": events, "form": form})


@login_required(login_url="base:login")
@user_passes_test(lambda user: user.is_superuser)
def createNews(request):
    if request.method == "POST":
        form = NewsCreationsForm(request.POST, request.FILES)
        if form.is_valid():
            logger.info(f"{request.user.fullName} is attempting to create a news update.")
            logger.info(form.cleaned_data)
            image = form.cleaned_data.get("image")
            title = str(form.cleaned_data.get("title")).capitalize().strip()
            resized_image = resizeImage(image, width=1000, height=800)
            news = form.save(commit=False)
            news.image = resized_image
            news.save()
            logger.info(f"News '{title}' has been posted.")
            messages.success(request, f"News '{title}' has been posted.")
            return redirect("news:createNews")
        else:
            displayFormErrors(request, form, messages, logger)
    else:
        form = NewsCreationsForm(initial={"session": request.user.getFullName})
    return render(request, "./news/pages/createNews.html", context={"form": form})


@login_required(login_url="base:login")
@user_passes_test(lambda user: user.is_superuser)
def createEvent(request):
    current_session = Session.objects.latest("created_on")
    if request.method == "POST":
        form = EventCreationForm(request.POST, request.FILES)
        if form.is_valid():
            title = str(form.cleaned_data.get("title")).capitalize().strip()
            image = form.cleaned_data.get("image")
            resized_image = resizeImage(image, width=1000, height=800) 
            event = form.save(commit=False)
            event.image = resized_image
            event.save()
            logger.info(f"News '{title}' has been posted.")
            messages.success(request, f"News '{title}' has been posted.")
            return redirect("news:createEvent")
        else:
            displayFormErrors(request, form, messages, logger)
    else:
        form = EventCreationForm(initial={"session": current_session})
    return render(request, "./news/pages/createEvent.html", context={"form": form})

