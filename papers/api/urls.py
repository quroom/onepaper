from django.urls import include, path
from rest_framework.routers import DefaultRouter
from papers.api.views import PaperViewset

router = DefaultRouter()
router.register(r"papers", PaperViewset)
urlpatterns = [    
    path("", include(router.urls)),
]