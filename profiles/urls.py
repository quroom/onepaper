from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import CustomUserViewset, CurrentProfileViewset, AllowedUserDetail, AllowedProfileList

router = DefaultRouter()
router.register(r"user", CustomUserViewset, basename="user")
router.register(r"profiles", CurrentProfileViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("profiles/<int:pk>/allowed-users/", AllowedUserDetail.as_view(), name="allowed-user-detail"),
    path("allowed-profiles/", AllowedProfileList.as_view(), name="allowed-profiles-list")
    # path("profiles/", ProfileViewset.as_view({"get": "list"}), name="profile-list"),
    # path("profiles/<int:pk>/", ProfileViewset.as_view({"get": "retrieve"}), name="profile-detail")
]