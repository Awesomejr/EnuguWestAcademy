import logging

from django.shortcuts import render

from base.models import ClassName
from library.models import Book


logger = logging.getLogger(__name__)

# Create your views here.
def books(request):
    all_class = ClassName.objects.all().order_by("name")
    search_title = request.GET.get("q")

    if search_title == None:
        # books = Book.objects.all().order_by("-created_on")
        books = Book.objects.all().order_by("?")
    else:
        # books = Book.objects.filter(title__icontains=search_title).order_by("-created_on")
        books = Book.objects.filter(title__icontains=search_title).order_by("?")

    context = {"books": books, "all_class": all_class}
    return render(request, "./library/pages/books.html", context=context)


# def previewBook(request):
#     pass


def sortByClass(request):
    books = Book.objects.all().order_by("-assigned_class")
    context = {"books": books}
    return render(request, "./library/components/bookCard.html", context=context)


def sortBySubject(request):
    books = Book.objects.all().order_by("subject")
    context = {"books": books}
    return render(request, "./library/components/bookCard.html", context=context)


def sortByNewest(request):
    books = Book.objects.all().order_by("-created_on")
    context = {"books": books}
    return render(request, "./library/components/bookCard.html", context=context)



# def filterByClass(request):
#     ...