from django.urls import include, path
from rest_framework.routers import DefaultRouter

from helps.views import NoticeGenericVieset

router = DefaultRouter()
router.register(r"notices", NoticeGenericVieset, basename="notices")
urlpatterns = [path("", include(router.urls))]
