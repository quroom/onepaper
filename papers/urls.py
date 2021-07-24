from django.urls import include, path
from rest_framework.routers import DefaultRouter
from papers.views import AllowPaperAPIView, AllPaperList, HidePaperAPIView, PaperViewset, PaperLoadAPIView, ExplanationSignatureCreateAPIView, ExplanationSignatureUpdateAPIView, SignatureCreateAPIView, SignatureUpdateAPIView

router = DefaultRouter()
router.register(r"papers", PaperViewset, basename="papers")
urlpatterns = [
    path("", include(router.urls)),
    path("all-papers/",
         AllPaperList.as_view(),
         name="all-papers"),
    path("papers/<int:pk>/load/",
          PaperLoadAPIView.as_view(),
          name="load-paper"),
    path("papers/<int:paper_id>/signatures/<int:pk>/",
          SignatureUpdateAPIView.as_view(),
          name="update-signature"),
    path("papers/<int:id>/signature/",
         SignatureCreateAPIView.as_view(),
         name="create-signature"),
    path("papers/<int:paper_id>/explanation-signatures/<int:pk>/",
          ExplanationSignatureUpdateAPIView.as_view(),
          name="update-explanation-signature"),
    path("papers/<int:id>/explanation-signature/",
          ExplanationSignatureCreateAPIView.as_view(),
          name="create-explanation-signature"),
    path("contractors/<int:pk>/allow-paper/",
          AllowPaperAPIView.as_view(),
          name="allow-paper"),
    path("contractors/<int:pk>/hide-paper/",
          HidePaperAPIView.as_view(),
          name="hide-paper")
]