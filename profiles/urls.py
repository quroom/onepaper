from django.urls import path, include
from rest_framework.routers import DefaultRouter
from profiles.views import AllowedProfileList, AllowedUserDetail, ApproveExpert, CustomUserViewset, ProfileViewset, SetDefaultProfile, MandateViewset, OpenProfileList, OpenProfileDetail

router = DefaultRouter()
router.register(r"user", CustomUserViewset, basename="user")
router.register(r"profiles", ProfileViewset, basename="profiles")
router.register(r"mandates", MandateViewset, basename="mandates")

urlpatterns = [
    path("", include(router.urls)),
    path("open-profiles/", OpenProfileList.as_view(), name="open-profiles"),
    path("open-profiles/<int:pk>/", OpenProfileDetail.as_view(), name="open-profile"),
    path("profiles/<int:pk>/default/", SetDefaultProfile.as_view(), name="default-profile"),
    path("profiles/<int:pk>/allowed-users/", AllowedUserDetail.as_view(), name="allowed-user-detail"),
    path("allowed-profiles/", AllowedProfileList.as_view(), name="allowed-profiles-list"),
    path("approve-experts/", ApproveExpert.as_view(), name="approve-expert")
]