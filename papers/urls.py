from django.urls import include, path
from rest_framework.routers import DefaultRouter
from papers.views import PaperViewset, PaperListApiView, SignatureCreateApiView, SignatureUpdateApiView, HidePaperApiView

router = DefaultRouter()
router.register(r"papers", PaperViewset, basename="Paper")
urlpatterns = [    
    path("", include(router.urls)),
    path("paper-list/",
          PaperListApiView.as_view()),    
    path("papers/<int:pk>/hide/",
         HidePaperApiView.as_view()),
    path("papers/<int:id>/signature/",
         SignatureCreateApiView.as_view(),
         name="create-signature"),
    path("papers/<int:paper_id>/signatures/<int:pk>/",
          SignatureUpdateApiView.as_view(),
          name="update-signature")
]