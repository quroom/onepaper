"""onepaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import debug_toolbar
from allauth.account.views import SignupView
from django.contrib import admin
from django.urls import include, path, re_path

from core.views import EmailConfirmedView, IndexTemplateView, IntroPageView
from profiles.forms import CustomUserForm, ExpertCustomUserForm

# https://django-registration.readthedocs.io/en/3.1/activation-workflow.html

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", IntroPageView.as_view()),
    path("accounts/", include("allauth.urls")),
    path("api/", include("profiles.urls")),
    path("api/", include("papers.urls")),
    path("api/", include("helps.urls")),
    path("intro/", IntroPageView.as_view(), name="onepaper_intro"),
    path("__debug__/", include(debug_toolbar.urls)),
    path("summernote/", include("django_summernote.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += (re_path(r"^.*$", IndexTemplateView.as_view(), name="entry-point"),)
