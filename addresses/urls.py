from django.urls import path

from addresses.views import DongAPIView

urlpatterns = [path("dongs/", DongAPIView.as_view(), name="dongs-list")]
