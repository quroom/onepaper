from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from profiles.views import (
    ActivateProfile,
    AllowedProfileList,
    AllowedUserDetail,
    ApproveExpert,
    CertificateAPIView,
    CustomUserViewset,
    ExpertProfileList,
    InsuranceViewset,
    MandateViewset,
    OpenProfileDetail,
    OpenProfileList,
    ProfileViewset,
    UserSettingAPIView,
)

router = routers.SimpleRouter()
router.register(r"mandates", MandateViewset, basename="mandates")
router.register(r"profiles", ProfileViewset, basename="profiles")
router.register(r"user", CustomUserViewset, basename="user")

profile_router = routers.NestedSimpleRouter(router, r"profiles", lookup="profile")
profile_router.register(r"insurances", InsuranceViewset, basename="profile-insurances")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(profile_router.urls)),
    path(
        "certification/",
        CertificateAPIView.as_view(),
        name="profile-certification",
    ),
    path("expert-profiles/", ExpertProfileList.as_view(), name="expert-profiles"),
    path("open-profiles/", OpenProfileList.as_view(), name="open-profiles"),
    path("open-profiles/<int:pk>/", OpenProfileDetail.as_view(), name="open-profile"),
    path("profiles/<int:pk>/activate/", ActivateProfile.as_view(), name="activate-profile"),
    path(
        "profiles/<int:pk>/allowed-users/", AllowedUserDetail.as_view(), name="allowed-user-detail"
    ),
    path("allowed-profiles/", AllowedProfileList.as_view(), name="allowed-profiles-list"),
    path("approve-experts/", ApproveExpert.as_view(), name="approve-expert"),
    path("user-setting/", UserSettingAPIView.as_view(), name="user-setting"),
]
