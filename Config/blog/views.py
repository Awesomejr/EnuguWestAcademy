import logging
import random
from pprint import pprint

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import ListView

from blog.models import Blog, Category, Comment
from blog.forms import PostForm
from base.models import CustomUser
from base.forms import LoginForm
from utilities import customFuncs
from utilities.testData import testData


logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    page_paginator = None
    number_of_items_per_page = 21
    categories = Category.objects.all()
    search_input = request.GET.get("q")
    page = request.GET.get("page")

    # testData.createBlogs(Model=Blog, number_of_blogs=600)


    if search_input:
        page_paginator = Paginator(Blog.objects.filter(
            Q(category__name__icontains=search_input) | Q(title__icontains=search_input) | 
            Q(author__first_name__icontains=search_input) | Q(author__last_name__icontains=search_input) | 
            Q(author__username__icontains=search_input) | Q(subject__name__icontains=search_input), 
            published=True
        ).select_related("category", "author", "assigned_class", "subject"), number_of_items_per_page)
    else:
        page_paginator = Paginator(Blog.objects.filter(published=True).select_related(
                            "category", "author", "assigned_class", "subject"
                            ), 
                            number_of_items_per_page
                        )

    blogs = page_paginator.get_page(page)

    form = LoginForm()

    context = {"blogs": blogs, "querysets": categories, "number_of_items_per_page": number_of_items_per_page, "form": form}
    return render(request, "./blog/pages/index.html", context=context)


def viewBlog(request, blogId):
    post = Blog.objects.select_related("author", "assigned_class", "subject", "category").get(id=blogId)
    related_posts = Blog.objects.filter(category=post.category, assigned_class=post.assigned_class).select_related(
                            "category", "author", "assigned_class", "subject"
                            ).order_by("?")[:10]

    context = {"post": post, "comments": post.comments.all(), "blogs": related_posts}
    return render(request, "./blog/pages/viewBlog.html", context=context)


@login_required(login_url="base:home")
def createBlog(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = CustomUser.objects.get(id=request.user.id)
            post.save()
            logger.info(f"Blog post '{str(post.title).capitalize()}' uploaded.")
            messages.success(request, f"Blog post '{str(post.title).capitalize()}' uploaded.")
            return redirect("blog:home")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)
    else:
        form = PostForm()
        # testData.createBlogs(Model=Blog)

    context = {"form": form, "title": "Create Blog Post"}
    return render(request, "./blog/pages/createUpdateBlog.html", context=context)


@login_required(login_url="base:home")
def editBlog(request, blogId):
    instance = Blog.objects.get(id=blogId)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            logger.info(f"Blog post updated.")
            messages.success(request, f"Blog post updated.")
            return redirect("blog:home")
        else:
            customFuncs.displayFormErrors(request, form, messages, logger)

    else:
        form = PostForm(instance=instance)

    context = {"form": form, "title": "Update Blog Post", "cover_image": instance.cover_image.url}
    return render(request, "./blog/pages/createUpdateBlog.html", context=context)


@login_required(login_url="base:home")
def deleteBlog(request, blogId):
    blog = Blog.objects.get(id=blogId)
    profile = CustomUser.objects.get(id=request.user.id)

    if blog.author != profile:
        logger.info(f"You do not have the required permissions to delete this post.")
        messages.warning(request, f"You do not have the required permissions to delete this post.")
        return redirect("blog:home")
    else:
        blog.delete()
        logger.info(f"blog deleted.")
        messages.success(request, f"blog deleted.")
    

    if request.htmx:
        return HttpResponse("")
    else:
        return redirect("blog:home")
    


def createComment(request, blogId):
    post = Blog.objects.get(id=blogId)
    user = CustomUser.objects.get(id=request.user.id)

    comment_text = request.POST.get("comment")
    Comment.objects.create(post=post, author=user, content=comment_text)

    comments = Comment.objects.filter(post=post)
    return render(request, "./blog/components/comments.html", context = {"post": post, "comments": comments})



def likePost(request, blogId):
    post = Blog.objects.get(id=blogId)
    # user = CustomUser.objects.get(id=request.user.id)

    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    return render(request, "./blog/components/likePost.html", context = {"post": post})
    

        




