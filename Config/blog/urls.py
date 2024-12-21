from django.urls import path
from blog import views

app_name = "blog"

urlpatterns = [
    path("blogs/", views.index, name="home"),
    path("view-blog/<str:blogId>/", views.viewBlog, name="viewBlog"),

    path("create-blog/", views.createBlog, name="createBlog"),
    path("edit-blog/<uuid:blogId>/", views.editBlog, name="editBlog"),
    path("delete-blog/<uuid:blogId>/", views.deleteBlog, name="deleteBlog"),
    path("like-post/<uuid:blogId>/", views.likePost, name="likePost"),

    path("create-comment/<uuid:blogId>/", views.createComment, name="createComment"),
]