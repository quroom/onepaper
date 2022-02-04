from django.urls import include, path
from rest_framework_nested import routers

from listings.views import ListingViewset

router = routers.SimpleRouter()
router.register(r"listings", ListingViewset, basename="listings")

urlpatterns = [path("", include(router.urls))]
