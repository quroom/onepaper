from django.urls import include, path
from rest_framework.routers import DefaultRouter
from papers.views import PaperViewset, SignatureViewSet

router = DefaultRouter()
router.register(r"papers", PaperViewset, basename="Paper")
urlpatterns = [    
    path("", include(router.urls)),
    path("papers/<int:id>/signature/",
         SignatureViewSet.as_view(),
         name="create-signature")
]