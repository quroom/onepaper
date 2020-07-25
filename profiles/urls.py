from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import CustomUserViewset, ProfileViewset

router = DefaultRouter()
router.register(r"user", CustomUserViewset, basename="user")
router.register(r"profiles", ProfileViewset)

urlpatterns = [
    path("", include(router.urls)),
    # path("profile/", CurrentProfileAPIView.as_view(), name="current-user"),
    # path("profiles/", ProfileViewset.as_view({"get": "list"}), name="profile-list"),
    # path("profiles/<int:pk>/", ProfileViewset.as_view({"get": "retrieve"}), name="profile-detail")
]