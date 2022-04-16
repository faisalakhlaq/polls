from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import VoterViewSet


app_name = "voters"

router = SimpleRouter()
router.register("voters", VoterViewSet, basename="voters")

urlpatterns = [path("", include(router.urls))]
