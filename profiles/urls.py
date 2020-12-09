from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import AllowedProfileList, AllowedUserDetail, ApproveExpert, CustomUserViewset, CurrentProfileViewset, HideProfileApiView, MandateViewset, MandateAllowedProfileDetail, ProfileDetailAPIView

router = DefaultRouter()
router.register(r"user", CustomUserViewset, basename="user")
router.register(r"profiles", CurrentProfileViewset, basename="profiles")
router.register(r"mandates", MandateViewset, basename="mandates")

urlpatterns = [
    path("", include(router.urls)),
    path("open-profiles/<int:pk>/", ProfileDetailAPIView.as_view(), name="open-profile"),
    path("profiles/<int:pk>/hide/", HideProfileApiView.as_view(), name="hide-profile"),
    path("profiles/<int:pk>/allowed-users/", AllowedUserDetail.as_view(), name="allowed-user-detail"),
    path("profiles/<int:pk>/allowed-mandates/", MandateAllowedProfileDetail.as_view(), name="allowed-mandates"),
    path("allowed-profiles/", AllowedProfileList.as_view(), name="allowed-profiles-list"),
    path("approve-experts/", ApproveExpert.as_view(), name="approve-expert")
    # path("profiles/", ProfileViewset.as_view({"get": "list"}), name="profile-list"),
    # path("profiles/<int:pk>/", ProfileViewset.as_view({"get": "retrieve"}), name="profile-detail")
]