from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import AuthedProfileList, CustomUserViewset, CurrentProfileViewset

router = DefaultRouter()
router.register(r"user", CustomUserViewset, basename="user")
router.register(r"profiles", CurrentProfileViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("authed-profiles/", AuthedProfileList.as_view(), name="authed-profiles"),
    # path("profiles/", ProfileViewset.as_view({"get": "list"}), name="profile-list"),
    # path("profiles/<int:pk>/", ProfileViewset.as_view({"get": "retrieve"}), name="profile-detail")
]