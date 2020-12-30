from django.urls import include, path
from rest_framework.routers import DefaultRouter
from papers.views import PaperViewset, PaperLoadAPIView, ExplanationSignatureCreateApiView, ExplanationSignatureUpdateApiView, SignatureCreateApiView, SignatureUpdateApiView, HidePaperApiView

router = DefaultRouter()
router.register(r"papers", PaperViewset, basename="papers")
urlpatterns = [    
    path("", include(router.urls)),
    path("papers/<int:pk>/load/",
          PaperLoadAPIView.as_view(),
          name="load-paper"),
    path("papers/<int:pk>/hide/",
          HidePaperApiView.as_view(),
          name="hide-paper"),
    path("papers/<int:paper_id>/signatures/<int:pk>/",
          SignatureUpdateApiView.as_view(),
          name="update-signature"),
    path("papers/<int:id>/signature/",
         SignatureCreateApiView.as_view(),
         name="create-signature"),
    path("papers/<int:paper_id>/explanation-signatures/<int:pk>/",
          ExplanationSignatureUpdateApiView.as_view(),
          name="update-explanation-signature"),
    path("papers/<int:id>/explanation-signature/",
          ExplanationSignatureCreateApiView.as_view(),
          name="create-explanation-signature")
]