"""django_vite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

# from apps.blog.sitemaps import PostSitemap
from config import settings

sitemaps = {
    # "posts": PostSitemap,
}

DJANGO_URLS = [
    # ------------------------------------------------------------
    # Django admin
    # ------------------------------------------------------------
    path("admin/", admin.site.urls),
    # ------------------------------------------------------------
    # Site paths
    # ------------------------------------------------------------
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

FLY_URLS = [
    # ------------------------------------------------------------
    # Fly apps
    # ------------------------------------------------------------
    path("", include("core.urls")),
    path("accounts/", include("account.urls")),
]

THIRD_PARTY_URLS = [
    path("__debug__/", include("debug_toolbar.urls")),
]

LOCAL_URLS = [
    # ------------------------------------------------------------
    # Local apps
    # ------------------------------------------------------------
]

urlpatterns = DJANGO_URLS + FLY_URLS + THIRD_PARTY_URLS + LOCAL_URLS

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
