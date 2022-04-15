from django.urls import include, path
from rest_framework_nested import routers

from listings.views import AskListingViewset, ListingStatusAPIView, ListingViewset

router = routers.SimpleRouter()
router.register(r"asklistings", AskListingViewset, basename="asklistings")
router.register(r"listings", ListingViewset, basename="listings")

urlpatterns = [
    path("", include(router.urls)),
    path("listings/<int:pk>/status/", ListingStatusAPIView.as_view(), name="update-status"),
]
