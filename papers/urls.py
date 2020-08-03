from django.urls import include, path
from rest_framework.routers import DefaultRouter
from papers.views import PaperViewset, SignatureListApiView, SignatureCreateApiView, HidePaperApiView

router = DefaultRouter()
router.register(r"papers", PaperViewset, basename="Paper")
urlpatterns = [    
    path("", include(router.urls)),
    path("papers/<int:pk>/hide/",
         HidePaperApiView.as_view()),
    path("papers/<int:id>/signatures/",
          SignatureListApiView.as_view(),
          name="retreive-signature"),
    path("papers/<int:id>/signature/",
         SignatureCreateApiView.as_view(),
         name="create-signature")
]