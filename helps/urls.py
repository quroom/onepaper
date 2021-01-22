from django.urls import include, path
from rest_framework.routers import DefaultRouter
from helps.views import NoticeGenericVieset, ManualGenericVieset

router = DefaultRouter()
router.register(r"notices", NoticeGenericVieset, basename="notices")
router.register(r"manuals", ManualGenericVieset, basename="manuals")
urlpatterns = [
     path("", include(router.urls))
]
