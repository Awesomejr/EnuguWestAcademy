"""
URL configuration for Config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('hijack/', include('hijack.urls')),
    path("", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path("", include("base.urls")),
    path("tech-support/", include("techSupport.urls")),
    path("student/", include("student.urls")),
    path("teacher/", include("teacher.urls")),
    path("guest/", include("guest.urls")),
    path("manager/", include("manager.urls")),
    path("examination/", include("examination.urls")),

    path("gallery/", include("gallery.urls")),
    path("news/", include("news.urls")),
    path("e-library/", include("library.urls")),
    path("blog/", include("blog.urls")),

    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += debug_toolbar_urls()